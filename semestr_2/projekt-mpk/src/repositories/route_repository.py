from datetime import timedelta
from typing import Set

from sanic.log import logger
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.model.database.model import (
    Route as DBRoute,
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
            route_stops_ids = {stop.stop_id for stop in route.stops}

            stops_statement = select(DBStop).where(DBRoute.id.in_(route_stops_ids))
            stops = list((await session.scalars(stops_statement)).unique())

            stops_times_statement = select(DBStopTimes).where(
                DBStopTimes.start_stop_id.in_(route_stops_ids)
            )
            stops_times = list(await (session.scalars(stops_times_statement)))

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

            logger.debug(f"id_to_domain_stops {id_to_domain_stops}")
            stops_domain_stops = []
            for route_stop in route.stops:
                logger.debug(f"Route stops | {route_stop.stop_id}")
                stops_domain_stops.append(id_to_domain_stops[route_stop.stop_id])
            transits = [
                Transit(id=transit.id,
                        start_time=transit.start_time,
                        route=route.id
                        )
                for transit in route.transits
            ]
            return DomainRoute(
                name=route.name, id=route.id, stops=stops_domain_stops, transits=transits
            )

    async def get_all(self) -> Set[DomainRoute]:
        async with self.session_maker() as session, session.begin():
            stops_statement = select(DBStop)
            stops = await session.scalars(stops_statement)

            stops_times_statement = select(DBStopTimes)
            stops_times = list(await session.scalars(stops_times_statement))
            domain_routes = set()
            routes_statement = select(DBRoute).order_by(DBRoute.name)
            routes = await session.scalars(routes_statement)

            # logger.debug("Stop time | {stop_time.id} | {stop_time.start_stop_id} | {stop_time.end_stop_id}")
            # for stop_time in stops_times:
                # logger.debug(f"Stop time | {stop_time.id} | {stop_time.start_stop_id} | {stop_time.end_stop_id}")
            for route in routes.unique():
                id_to_domain_stops = {}
                for stop in stops.unique():

                    time_to_other_stops = {}
                    for stop_time in stops_times:
                        # logger.debug(f"Stop.id = {stop.id} | stop_time.start_stop_id={stop_time.start_stop_id}")
                        if stop_time.start_stop_id == stop.id:
                            # logger.debug(f"Time to next stop {stop_time.end_stop_id}->{stop_time.start_stop_id}")
                            time_to_other_stops[str(stop_time.end_stop_id)] = timedelta(
                                seconds=stop_time.time_in_seconds
                            )
                    id_to_domain_stops[stop.id] = DomainStop(
                        id=stop.id,
                        name=stop.name,
                        loc_y=stop.loc_y,
                        loc_x=stop.loc_x,
                        time_to_other_stops=time_to_other_stops,
                    )

                logger.debug(f"id_to_domain_stops {id_to_domain_stops}")
                domain_stops = [id_to_domain_stops.get(stop.id) for stop in route.stops]
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

            stops_statement = select(DBStop)
            stops = await session.scalars(stops_statement)

            stops_times_statement = select(DBStopTimes)
            stops_times = list((await session.scalars(stops_times_statement)).all())
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
                    for stop in stops.all()
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
            await session.commit()
            return domain_routes

    async def delete(self, route_id: str):
        async with self.session_maker() as session, session.begin():
            delete_stop_statement = delete(DBRoute).where(DBRoute.id == int(route_id))
            await session.execute(delete_stop_statement)
            await session.commit()
