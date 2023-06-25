from datetime import timedelta

from src.model.database.model import Stop as StopDB
from src.model.domain_model import Stop as DomainStop, Transit as DomainTransit


async def db_stop_to_domain(stop: StopDB) -> DomainStop:
    domain_stop = DomainStop(
        id=stop.id,
        name=stop.name,
        loc_y=stop.loc_y,
        loc_x=stop.loc_x,
        time_to_other_stops={
            str(stop_time.end_stop_id): timedelta(
                seconds=stop_time.time_in_seconds
            )
            for stop_time in stop.stop_times
            if stop_time.start_stop_id == stop.id
        },
    )
    return domain_stop


async def db_transit_to_domain(new_transit):
    domain_transit = DomainTransit(
        id=new_transit.id,
        route=DomainRoute(
            id=new_transit.route_id,
            name=new_transit.route.name,
            stops=[await db_stop_to_domain(stop) for stop in new_transit.route.stops]
        ),
        start_time=new_transit.start_time,


    )
    return domain_transit