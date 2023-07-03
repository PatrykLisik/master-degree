from datetime import timedelta
from typing import Set

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.model.database.model import (
    Route as DBRoute,
    RouteStop as DBRouteStop,
    StopTimes as DBStopTimes,
    Stop as DBStop
)
from src.model.domain_model import Route as DomainRoute, Stop as DomainStop, Transit
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
            transits = [
                Transit(id=transit.id,
                        start_time=transit.start_time,
                        route=route.id
                        )
                for transit in route.transits
            ]
            return DomainRoute(
                name=route.name, id=route.id, stops=stops, transits=transits
            )

    async def get_all(self) -> Set[DomainRoute]:
        async with self.session_maker() as session, session.begin():
            stops_statement = select(DBStop)
            stops = await session.scalars(stops_statement)

            stops_times_statement = select(DBStopTimes)
            stops_times = await session.scalars(stops_times_statement)
            domain_routes = set()
            routes_statement = select(DBRoute).order_by(DBRoute.name)
            routes = await session.scalars(routes_statement)
            for route in routes.unique():
                id_to_domain_stops = {
                    stop.id: DomainStop(
                        id=stop.id,
                        name="",
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
                    for stop in stops.unique()
                }

                domain_stops = [id_to_domain_stops[stop.id] for stop in route.stops]
                transits = [
                    Transit(
                        id=transit.id, start_time=transit.start_time, route=route.id
                    )
                    for transit in route.transits
                ]
                domain_route = DomainRoute(
                    name=route.name, id=route.id, stops=domain_stops, transits=transits
                )
                domain_routes.add(domain_route)
            return domain_routes

    async def search_by_name(self, query) -> Set[DomainRoute]:
        async with self.session_maker() as session, session.begin():
            select_all_routes_statement = select(DBRoute).where(
                DBRoute.name.like(query)
            )
            db_routes = await session.scalars(select_all_routes_statement)

            stops_statement = select(DBRouteStop)
            stops = await session.scalars(stops_statement)

            stops_times_statement = select(DBStopTimes)
            stops_times = await session.scalars(stops_times_statement)
            domain_routes = set()
            for route in db_routes.unique():
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
                transits = [
                    Transit(
                        id=transit.id, start_time=transit.start_time, route=route.id
                    )
                    for transit in route.transits
                ]
                domain_route = DomainRoute(
                    name=route.name, id=route.id, stops=stops, transits=transits
                )
                domain_routes.add(domain_route)
            await session.commit()
            return domain_routes

    async def delete(self, route_id: str):
        async with self.session_maker() as session, session.begin():
            delete_stop_statement = delete(DBRoute).where(DBRoute.id == int(route_id))
            await session.execute(delete_stop_statement)
            await session.commit()
