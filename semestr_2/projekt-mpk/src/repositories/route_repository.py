import json
import uuid
from dataclasses import asdict
from datetime import timedelta
from typing import Dict, Optional, Set

from sanic.log import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.model.database.model import (
    Route as DBRoute,
    RouteStop as DBRouteStop,
    StopTimes as DBStopTimes,
)
from src.model.domain_model import Route as DomainRoute, Stop as DomainStop
from src.model.infile.infile_mappers import domain_route_to_infile, infile_route_to_domain
from src.model.infile.infile_model import Route
from src.repositories.abstract import AbstractRouteRepository, AbstractStopRepository


class InFileRouteRepository(AbstractRouteRepository):
    _file_name = "data/routes.json"

    def __init__(self, stops_repository: AbstractStopRepository):
        super()
        self.stops_repository = stops_repository

    def _get(self) -> Dict[str, Route]:
        try:
            with open(
                self._file_name,
                "r+",
            ) as infile:
                logger.info("load routes")
                data = json.load(infile)
                return {route_data["id"]: Route(**route_data) for route_data in data}
        except FileNotFoundError:
            logger.info("file doest not exist")
            return {}

    def _set(self, routes: Dict[str, Route]):
        logger.info("save routes")
        drivers_to_save = [asdict(route) for route in routes.values()]
        json_to_save = json.dumps(drivers_to_save, indent=4)
        with open(self._file_name, "w+") as outfile:
            outfile.write(json_to_save)

    async def add(self, name: str, stops: list[str]) -> DomainRoute:
        new_route = Route(name=name, stops=stops, id=str(uuid.uuid4()))
        routes = self._get()
        routes[new_route.id] = new_route
        self._set(routes)
        return await infile_route_to_domain(new_route, self.stops_repository)

    async def update(self, route_id: str, updated_route: DomainRoute):
        self._get()[route_id] = await domain_route_to_infile(updated_route)

    async def get(self, route_id: str) -> Optional[DomainRoute]:
        route = self._get().get(route_id, None)
        if route is None:
            return None
        return await infile_route_to_domain(route, self.stops_repository)

    async def get_all(self) -> Set[DomainRoute]:
        return {
            await infile_route_to_domain(route, self.stops_repository)
            for route in self._get().values()
        }


class DatabaseRouteRepository(AbstractRouteRepository):

    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        self.session_maker = session_maker

    async def add(self, name: str, stops: list[str]) -> DomainRoute:
        async with self.session_maker() as session:
            async with session.begin():
                new_route = DBRoute(name=name, stops=[])  # assume no stops
                session.add(new_route)
                await session.flush()
                domain_route = DomainRoute(
                    stops=[], id=str(new_route.id), name=new_route.name
                )
            await session.commit()
        return domain_route

    async def update(self, route_id: str, updated_route: DomainRoute):
        async with self.session_maker() as session:
            async with session.begin():
                route = await session.get(DBRoute, int(route_id))
                route.name = updated_route.name
                route.stops = [
                    DBRouteStop(id=stop.id, order=index)
                    for index, stop in enumerate(updated_route.stops)
                ]
            await session.commit()

    async def get(self, route_id: str) -> DomainRoute:
        async with self.session_maker() as session:
            route = await session.get(
                DBRoute, int(route_id), populate_existing=True
            )
            route_stops_ids = {stop.id for stop in route.stops}

            stops_statement = select(DBRouteStop).where(
                DBRoute.id.in_(route_stops_ids)
            )
            stops = await session.scalars(stops_statement)

            stops_times_statement = select(DBStopTimes).where(
                DBStopTimes.start_stop_id.in_(route_stops_ids)
            )
            stops_times = await session.scalars(stops_times_statement)

            id_to_domain_stops = {
                stop.id: DomainStop(
                    id=stop.id,
                    name=stop.name,
                    loc_y=str(stop.loc_y),
                    loc_x=str(stop.loc_x),
                    time_to_other_stops={
                        str(stop_time.end_stop_id): timedelta(
                            seconds=stop_time.time_in_seconds
                        )
                        for stop_time in stops_times
                        if stop_time.start_stop_id == stop.id
                    },
                )
                for stop in stops
            }

            stops = [id_to_domain_stops[stop.id] for stop in route.stops]
            return DomainRoute(name=route.name, id=route.id, stops=stops)

    async def get_all(self) -> Set[DomainRoute]:
        async with self.session_maker() as session:
            routes_statement = select(DBRoute)
            routes = await session.scalars(routes_statement)

            stops_statement = select(DBRouteStop)
            stops = await session.scalars(stops_statement)

            stops_times_statement = select(DBStopTimes)
            stops_times = await session.scalars(stops_times_statement)
            domain_routes = set()
            for route in routes:
                id_to_domain_stops = {
                    stop.id: DomainStop(
                        id=stop.id,
                        name=stop.name,
                        loc_y=stop.loc_y,
                        loc_x=stop.loc_x,
                        time_to_other_stops={
                            str(stop_time.end_stop_id): timedelta(
                                seconds=stop_time.time_in_seconds
                            )
                            for stop_time in stops_times
                            if stop_time.start_stop_id == stop.id
                        },
                    )
                    for stop in stops
                }

                stops = [id_to_domain_stops[stop.id] for stop in route.stops]
                domain_route = DomainRoute(name=route.name, id=route.id, stops=stops)
                domain_routes.add(domain_route)
            return domain_routes
