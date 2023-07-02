from datetime import timedelta
from datetime import timedelta
from typing import Set

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.model.database.model import (
    Route as DBRoute,
    RouteStop as DBRouteStop,
    StopTimes as DBStopTimes,
)
from src.model.domain_model import Route as DomainRoute, Stop as DomainStop
from src.repositories.abstract import AbstractRouteRepository


class DatabaseRouteRepository(AbstractRouteRepository):
    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        self.session_maker = session_maker

    async def add(self, name: str) -> DomainRoute:
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

    async def get(self, route_id: str) -> DomainRoute:
        async with self.session_maker() as session:
            route = await session.get(DBRoute, int(route_id), populate_existing=True)
            route_stops_ids = {stop.id for stop in route.stops}

            stops_statement = select(DBRouteStop).where(DBRoute.id.in_(route_stops_ids))
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
            for route in routes.unique():
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

    async def search(self, query: str) -> Set[DomainRoute]:
        return set()
