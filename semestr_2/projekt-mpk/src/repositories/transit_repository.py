import json
import uuid
from dataclasses import asdict
from datetime import datetime
from typing import Dict, Optional, Set

from sanic.log import logger

from src.model.database.to_domain_mappers import db_transit_to_domain
from src.model.domain_model import (
    Transit as DomainTransit
)
from src.model.database.model import Transit as DBTransit
from src.model.infile_mappers import infile_transit_to_domain
from src.model.infile_model import Transit
from src.repositories.abstract import (
    AbstractDriverRepository,
    AbstractRouteRepository,
    AbstractTransitRepository,
    AbstractVehicleRepository,
)
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select


class InFileTransitRepository(AbstractTransitRepository):
    _file_name = "data/transits.json"

    def __init__(
        self,
        route_repo: AbstractRouteRepository,
        driver_repo: AbstractDriverRepository,
        vehicle_repo: AbstractVehicleRepository,
    ):
        super(InFileTransitRepository)
        self._route_repo = route_repo
        self._driver_repo = driver_repo
        self._vehicle_repo = vehicle_repo

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
                        vehicle_id=transit_data["vehicle_id"],
                        driver_id=transit_data["driver_id"],
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
            vehicle_id=vehicle_id,
            driver_id=driver_id,
            id=str(uuid.uuid4()),
        )
        transits = self._get()
        transits[new_transit.id] = new_transit
        self._set(transits)
        return await infile_transit_to_domain(
            new_transit,
            route_repo=self._route_repo,
            driver_repo=self._driver_repo,
            vehicle_repo=self._vehicle_repo,
        )

    async def update(self, transit_id: str, updated_transit: DomainTransit):
        transits = self._get()
        transits[transit_id] = Transit(
            route_id=updated_transit.route.id,
            start_time=str(updated_transit.start_time),
            vehicle_id=updated_transit.vehicle.id,
            driver_id=updated_transit.driver.id,
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
            driver_repo=self._driver_repo,
            vehicle_repo=self._vehicle_repo,
        )

    async def get_all(self) -> Set[DomainTransit]:
        logger.debug(f"self._route_repo {type(self)}")
        return {
            await infile_transit_to_domain(
                transit=transit,
                route_repo=self._route_repo,
                driver_repo=self._driver_repo,
                vehicle_repo=self._vehicle_repo,
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

    async def add(self, route_id: str, start_time: datetime, vehicle_id: str, driver_id: str) -> DomainTransit:
        async with self.session_maker() as session:
            async with session.begin():
                new_transit = DBTransit(
                    start_time=start_time,
                    route_id=route_id,
                    vehicle_id=vehicle_id,
                    driver_id=driver_id
                )
                await session.flush()
                domain_transit = await db_transit_to_domain(new_transit)
                await session.commit()
                return domain_transit

    async def update(self, transit_id: str, updated_transit: DomainTransit):
        async with self.session_maker() as session:
            async with session.begin():
                new_transit = DBTransit(
                    start_time=updated_transit.start_time,
                    route_id=updated_transit.route.id,
                    vehicle_id=updated_transit.vehicle.id,
                    driver_id=updated_transit.driver.id
                )

            await session.commit()

    async def get(self, transit_id: str) -> DomainTransit:
        async with self.session_maker() as session:
            db_transit = session.get(DBTransit, transit_id)
            return await db_transit_to_domain(db_transit)

    async def get_all(self) -> Set[DomainTransit]:
        async with self.session_maker() as session:
            get_all_transit_statement = select(DBTransit)
            transits = await session.scalars(get_all_transit_statement)
            domain_transits = set()
            for db_transit in transits:
                domain_transits.add(await db_transit_to_domain(db_transit))
            return domain_transits

    async def get_by_route(self, route_id: str) -> Set[DomainTransit]:
        async with self.session_maker() as session:
            get_all_transit_statement = select(DBTransit).where(DBTransit.route_id == route_id)
            transits = await session.scalars(get_all_transit_statement)
            domain_transits = set()
            for db_transit in transits:
                domain_transits.add(await db_transit_to_domain(db_transit))
            return domain_transits
