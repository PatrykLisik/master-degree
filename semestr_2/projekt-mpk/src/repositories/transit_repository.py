import json
import uuid
from dataclasses import asdict
from datetime import datetime, time
from typing import Dict, Optional, Set

from sanic.log import logger
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.model.database.model import Transit as DBTransit
from src.model.domain_model import Transit as DomainTransit
from src.model.infile.infile_mappers import infile_transit_to_domain
from src.model.infile.infile_model import Transit
from src.repositories.abstract import (
    AbstractRouteRepository,
    AbstractTransitRepository,
)


class InFileTransitRepository(AbstractTransitRepository):
    _file_name = "data/transits.json"

    def __init__(
        self,
        route_repo: AbstractRouteRepository,
    ):
        super(InFileTransitRepository)
        self._route_repo = route_repo

    def _get(self) -> Dict[str, Transit]:
        try:
            with open(
                self._file_name,
                "r+",
            ) as infile:
                logger.info("load transit")
                data = json.load(infile)
                return {
                    transit_data["id"]: Transit(
                        id=transit_data["id"],
                        route_id=transit_data["route_id"],
                        start_time=transit_data["start_time"],
                    )
                    for transit_data in data
                }
        except FileNotFoundError:
            logger.info("load transit file doest not exist")
            return {}

    def _set(self, transits: Dict[str, Transit]):
        logger.info("save transits")
        transits_to_save = [asdict(transit) for transit in transits.values()]
        json_to_save = json.dumps(transits_to_save, indent=4, default=str)
        with open(self._file_name, "w+") as outfile:
            outfile.write(json_to_save)

    async def add(
        self, route_id: str, start_time: datetime, vehicle_id: str, driver_id: str
    ) -> DomainTransit:
        new_transit = Transit(
            route_id=route_id,
            start_time=str(start_time),
            id=str(uuid.uuid4()),
        )
        transits = self._get()
        transits[new_transit.id] = new_transit
        self._set(transits)
        return await infile_transit_to_domain(
            new_transit,
            route_repo=self._route_repo,
        )

    async def update(self, transit_id: str, updated_transit: DomainTransit):
        transits = self._get()
        transits[transit_id] = Transit(
            route_id=updated_transit.route.id,
            start_time=str(updated_transit.start_time),
            id=transit_id,
        )
        self._set(transits)

    async def get(self, transit_id: str) -> Optional[DomainTransit]:
        transit = self._get().get(transit_id, None)
        if transit is None:
            raise Exception("Transit not found")
        return await infile_transit_to_domain(
            transit,
            route_repo=self._route_repo,
        )

    async def get_all(self) -> Set[DomainTransit]:
        logger.debug(f"self._route_repo {type(self)}")
        return {
            await infile_transit_to_domain(
                transit=transit,
                route_repo=self._route_repo,
            )
            for transit in self._get().values()
        }

    async def get_by_route(self, route_id: str) -> Set[DomainTransit]:
        return {
            transit for transit in await self.get_all() if transit.route.id == route_id
        }


class DatabaseTransitRepository(AbstractTransitRepository):
    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        self.session_maker = session_maker

    async def add(self, route_id: str, start_time: time):
        async with self.session_maker() as session:
            new_transit = DBTransit(start_time=start_time, route_id=int(route_id))
            session.add(new_transit)
            await session.commit()

    async def delete(self, transit_id: str):
        async with self.session_maker() as session:
            delete_stop_statement = delete(DBTransit).where(DBTransit.id == int(transit_id))
            await session.execute(delete_stop_statement)
            await session.commit()
