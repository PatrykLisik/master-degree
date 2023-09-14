import decimal
from datetime import timedelta
from typing import Set

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.model.database.model import Stop as StopDB, StopTimes as StopTimesDB
from src.model.database.to_domain_mappers import db_stop_to_domain
from src.model.domain_model import Stop as DomainStop
from src.repositories.abstract import AbstractStopRepository


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
            await session.commit()

    async def search_by_name(self, query) -> Set[DomainStop]:
        async with self.session_maker() as session:
            select_all_stops_statement = select(StopDB).where(StopDB.name.ilike(query))
            db_stops = await session.scalars(select_all_stops_statement)

            domain_stops = set()
            for stop in db_stops.unique():
                domain_stop = db_stop_to_domain(stop)
                domain_stops.add(domain_stop)
            return domain_stops
