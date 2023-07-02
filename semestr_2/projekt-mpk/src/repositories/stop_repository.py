import decimal
import json
import uuid
from datetime import timedelta
from typing import Dict, Set

from sanic.log import logger
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.model.database.model import Stop as StopDB, StopTimes as StopTimesDB
from src.model.database.to_domain_mappers import db_stop_to_domain
from src.model.domain_model import Stop as DomainStop
from src.model.infile.infile_mappers import infile_stop_to_domain
from src.model.infile.infile_model import Stop
from src.repositories.abstract import AbstractStopRepository


class InMemoryStopRepository(AbstractStopRepository):
    _stops: dict[str, Stop] = {}

    async def add(
        self, name: str, geolocation_x: decimal, geolocation_y: decimal
    ) -> DomainStop:
        new_stop = Stop(
            name=name,
            geolocation=(geolocation_x, geolocation_y),
            time_to_other_stops_in_seconds={},
            id=str(uuid.uuid4()),
        )
        self._stops[new_stop.id] = new_stop
        return await infile_stop_to_domain(new_stop)

    async def update(self, stop_id: str, updated_stop: DomainStop):
        self._stops[stop_id] = updated_stop

    async def get(self, stop_id: str) -> DomainStop:
        return await infile_stop_to_domain(self._stops[stop_id])

    async def get_all(self) -> Set[DomainStop]:
        return {await infile_stop_to_domain(stop) for stop in self._stops.values()}

    async def get_many(self, stop_ids: set[str]) -> Set[DomainStop]:
        return {
            await infile_stop_to_domain(value)
            for value in self._stops.values()
            if value.id in stop_ids
        }

    def set_time_between_stops(
        self, start_stop_id: str, end_stop_id: str, time: timedelta
    ):
        start_stop = self._stops.get(start_stop_id)
        start_stop.time_to_other_stops_in_seconds[end_stop_id] = time.seconds


class InFileStopRepository(AbstractStopRepository):
    _file_name = "data/stop.json"

    def _get_stops(self) -> Dict[str, Stop]:
        try:
            with open(
                self._file_name,
                "r+",
            ) as infile:
                logger.info("load stops")
                data = json.load(infile)
                return {
                    stop_data["id"]: Stop(
                        id=stop_data["id"],
                        name=stop_data["name"],
                        geolocation=(stop_data["x"], stop_data["y"]),
                        time_to_other_stops_in_seconds={
                            times["stop_id"]: int(times["time_in_sec"])
                            for times in stop_data["time_to_other_stops_in_seconds"]
                        },
                    )
                    for stop_data in data
                }
        except FileNotFoundError:
            logger.info("load stop file doest not exist")
            return {}

    def _set_stops(self, stops: Dict[str, Stop]):
        logger.info("save stops")
        stops_to_save = [
            {
                "id": stop.id,
                "name": stop.name,
                "x": stop.geolocation[0],
                "y": stop.geolocation[1],
                "time_to_other_stops_in_seconds": [
                    {"stop_id": stop_id, "time_in_sec": time_to_other_stop}
                    for stop_id, time_to_other_stop in stop.time_to_other_stops_in_seconds.items()
                ],
            }
            for stop in stops.values()
        ]
        json_to_save = json.dumps(stops_to_save, indent=4)
        with open(self._file_name, "w+") as outfile:
            outfile.write(json_to_save)

    async def add(
        self, name: str, geolocation_x: decimal, geolocation_y: decimal
    ) -> Stop:
        new_stop = Stop(
            name=name,
            geolocation=(geolocation_x, geolocation_y),
            time_to_other_stops_in_seconds={},
            id=str(uuid.uuid4()),
        )
        stops = self._get_stops()
        stops[new_stop.id] = new_stop
        self._set_stops(stops)
        return await infile_stop_to_domain(new_stop)

    async def update(self, stop_id: str, updated_stop: Stop):
        stops = self._get_stops()
        stops[stop_id] = updated_stop
        self._set_stops(stops)

    async def get(self, stop_id: str) -> Stop:
        return await infile_stop_to_domain(self._get_stops()[stop_id])

    async def get_all(self) -> Set[Stop]:
        return {
            await infile_stop_to_domain(stop) for stop in self._get_stops().values()
        }

    async def get_many(self, stop_ids: set[str]) -> Set[Stop]:
        return {
            await infile_stop_to_domain(value)
            for value in self._get_stops().values()
            if value.id in stop_ids
        }

    async def set_time_between_stops(
        self, start_stop_id: str, end_stop_id: str, time: timedelta
    ):
        stops = self._get_stops()
        start_stop = stops.get(start_stop_id)
        start_stop.time_to_other_stops_in_seconds[end_stop_id] = time.seconds
        stops[start_stop_id] = start_stop
        self._set_stops(stops)


class DatabaseStopRepository(AbstractStopRepository):
    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        self.session_maker = session_maker

    async def add(
        self, name: str, geolocation_x: decimal.Decimal, geolocation_y: decimal.Decimal
    ) -> DomainStop:
        async with self.session_maker() as session:
            async with session.begin():
                new_stop = StopDB(name=name, loc_x=geolocation_x, loc_y=geolocation_y)
                session.add(new_stop)
                await session.flush()
                domain_stop = DomainStop(
                    id=new_stop.id,
                    name=new_stop.name,
                    loc_x=new_stop.loc_x,
                    loc_y=new_stop.loc_y,
                )
            await session.commit()
        return domain_stop

    async def update(self, stop_id: str, updated_stop: DomainStop):
        async with self.session_maker() as session:
            stop = await session.get(StopDB, stop_id)
            stop.name = updated_stop.name
            stop.loc_y = updated_stop.loc_y
            stop.loc_x = updated_stop.loc_x

    async def get(self, stop_id: str) -> DomainStop:
        async with self.session_maker() as session:
            stop = await session.get(StopDB, int(stop_id))
            if stop is None:
                raise ValueError("Stop not found")
            return db_stop_to_domain(stop)

    async def get_all(self) -> Set[DomainStop]:
        async with self.session_maker() as session:
            select_all_stops_statement = select(StopDB).limit(8)
            db_stops = await session.scalars(select_all_stops_statement)

            domain_stops = set()
            for stop in db_stops.unique():
                domain_stop = db_stop_to_domain(stop)
                domain_stops.add(domain_stop)
            return domain_stops

    async def get_many(self, stop_ids: set[str]) -> Set[DomainStop]:
        async with self.session_maker() as session:
            select_all_stops_statement = select(StopDB).where(StopDB.id.in_(stop_ids))
            db_stops = await session.scalars(select_all_stops_statement)

            domain_stops = set()
            for stop in db_stops.unique():
                domain_stop = db_stop_to_domain(stop)
                domain_stops.add(domain_stop)
            return domain_stops

    async def set_time_between_stops(
        self, start_stop_id: str, end_stop_id: str, time: timedelta
    ):
        async with self.session_maker() as session:
            stop_time = StopTimesDB(
                start_stop_id=int(start_stop_id),
                end_stop_id=int(end_stop_id),
                time_in_seconds=int(time.total_seconds()),
            )
            session.add(stop_time)
            await session.commit()

    async def delete_time_between_stops(self, start_stop_id: str, end_stop_id: str):
        async with self.session_maker() as session:
            delete_times_between_stops_statement = delete(StopTimesDB).where(
                StopTimesDB.start_stop_id == int(start_stop_id)
                and StopTimesDB.end_stop_id == int(end_stop_id)
            )
            await session.execute(delete_times_between_stops_statement)

    async def delete(self, stop_id: str):
        async with self.session_maker() as session:
            delete_stop_statement = delete(StopDB).where(StopDB.id == int(stop_id))
            await session.execute(delete_stop_statement)

    async def search_by_name(self, query) -> Set[DomainStop]:
        async with self.session_maker() as session:
            select_all_stops_statement = select(StopDB).where(StopDB.name.like(query))
            db_stops = await session.scalars(select_all_stops_statement)

            domain_stops = set()
            for stop in db_stops.unique():
                domain_stop = db_stop_to_domain(stop)
                domain_stops.add(domain_stop)
            return domain_stops
