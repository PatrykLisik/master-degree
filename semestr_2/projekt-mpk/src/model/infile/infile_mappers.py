from datetime import datetime, timedelta

from src.model.domain_model import (
    Route as DomainRoute,
    Stop as DomainStop,
    Transit as DomainTransit,
)
from src.model.infile.infile_model import (
    Route as InfileRoute,
    Stop as InFileStop,
    Transit as InFileTransit,
)
from src.repositories.abstract import (
    AbstractRouteRepository,
    AbstractStopRepository,
)


async def infile_route_to_domain(
    route: InfileRoute, stops_repository: AbstractStopRepository
) -> DomainRoute:
    stop_ids = set(route.stops)
    stops = {stop.id: stop for stop in await stops_repository.get_many(stop_ids)}
    return DomainRoute(
        id=route.id, name=route.name, stops=[stops[stop_id] for stop_id in route.stops]
    )


async def domain_route_to_infile(route: DomainRoute) -> InfileRoute:
    return InfileRoute(
        name=route.name, id=route.id, stops=[stop.id for stop in route.stops]
    )


async def infile_stop_to_domain(stop: InFileStop) -> DomainStop:
    return DomainStop(
        name=stop.name,
        time_to_other_stops={
            stop_id: timedelta(seconds=time)
            for stop_id, time in stop.time_to_other_stops_in_seconds.items()
        },
        loc_x=stop.geolocation[0],
        loc_y=stop.geolocation[1],
        id=stop.id,
    )


async def domain_stop_to_infile(stop: DomainStop) -> InFileStop:
    return InFileStop(
        name=stop.name,
        time_to_other_stops_in_seconds={
            stop_id: time.seconds for stop_id, time in stop.time_to_other_stops.items()
        },
        id=stop.id,
        geolocation=[stop.loc_x, stop.loc_y],
    )


async def infile_transit_to_domain(
    transit: InFileTransit,
    route_repo: AbstractRouteRepository,
) -> DomainTransit:
    route = await route_repo.get(transit.route_id)
    return DomainTransit(
        id=transit.id,
        route=route,
        start_time=datetime.fromisoformat(transit.start_time),
    )
