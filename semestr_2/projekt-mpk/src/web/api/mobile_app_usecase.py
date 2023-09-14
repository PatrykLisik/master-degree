from datetime import datetime, timedelta, time, date
from typing import Iterable, List, TypeVar

from sanic.log import logger

from src.model.domain_model import Stop
from src.repositories.abstract import AbstractRouteRepository, AbstractTransitRepository


async def get_all_routes_usecase(
        route_repository: AbstractRouteRepository,
) -> dict[str, str]:
    routes = await route_repository.get_all()
    return {route.name: route.id for route in routes}


async def get_route_stops_usecase(
        route_repository: AbstractRouteRepository, route_id: str
) -> dict[str, str]:
    route = await route_repository.get(route_id=route_id)
    if not route:
        return {}
    return {stop.name: stop.id for stop in route.stops}


async def get_stop_timetable_usecase(
        route_repository: AbstractRouteRepository,
        transit_repository: AbstractTransitRepository,
        route_id: str,
        stop_id: str,
) -> List[time]:
    route = await route_repository.get(route_id=route_id)
    time_offset = _time_to_stop_on_list(stop_list=route.stops, target_stop_id=stop_id)
    logger.info(f"time_offset: {time_offset}")
    route_transits = route.transits
    return [(datetime.combine(date.today(), transit.start_time) + time_offset).time() for transit in route_transits]


T = TypeVar("T")


def pair_iterator(iterable: Iterable[T]) -> (T, T):
    """
    l = [1,2,3,4,5]
    for value1, value2 in pair_iterator(l):
        print(f"{value1} {value2}")

    1 2
    2 3
    3 4
    4 5
    :param iterable:
    :return:
    """
    closure_iterator = iter(iterable)
    current_value = next(closure_iterator)
    for next_value in closure_iterator:
        yield current_value, next_value
        current_value = next_value


def _time_to_stop_on_list(stop_list: List[Stop], target_stop_id) -> timedelta:
    # calculate offset from start
    offset: timedelta = timedelta()
    logger.debug(f"OFFSET | target_stop_id= {target_stop_id}")
    logger.debug(f"OFFSET| stop list {stop_list}")
    for stop, next_stop in pair_iterator(stop_list):
        try:
            delta = stop.time_to_other_stops[str(next_stop.id)]
        except KeyError:
            logger.error(f"Stop {stop.id} has no distance definition to {next_stop.id}")
            delta = timedelta()

        offset += delta
        logger.debug(f"Stop id= {stop.id} | offset = {offset}")
        if str(stop.id) == str(target_stop_id):
            return offset
    return offset


def time_delta_from_str(timedelta_string: str) -> timedelta:
    t = datetime.strptime(timedelta_string, "%H:%M:%S")
    delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
    return delta
