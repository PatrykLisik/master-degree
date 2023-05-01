from datetime import timedelta, datetime
from typing import List, Iterable, TypeVar

from sanic.log import logger

from src.model.domain_model import Route, Stop
from src.repositories.abstract import (
    AbstractRouteRepository,
    AbstractStopRepository,
    AbstractTransitRepository
)


def get_all_routes_usecase(route_repository: AbstractRouteRepository) -> dict[
    str, str]:
    return {route.name: route.id for route in route_repository.get_all()}


def get_route_stops_usecase(route_repository: AbstractRouteRepository,
                            route_id: str) -> list[(str, str)]:
    route = route_repository.get(route_id=route_id)
    return [(stop.name, stop.id) for stop in route.stops]


def get_stop_timetable_usecase(route_repository: AbstractRouteRepository,
                               transit_repository: AbstractTransitRepository,
                               route_id: str, stop_id: str) -> List[datetime]:
    route = route_repository.get(route_id=route_id)
    time_offset = _time_to_stop_on_list(stop_list=route.stops, target_stop_id=stop_id)
    logger.info(f"time_offset: {time_offset}")
    route_transits = [transit for transit in transit_repository.get_all() if transit.route.id == route_id]
    return [transit.start_time + time_offset for transit in route_transits]


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
    for stop, next_stop in pair_iterator(stop_list):
        if stop.id == target_stop_id:
            return offset
        delta = time_delta_from_str(stop.time_to_other_stops[next_stop.id])
        offset += delta
        if next_stop.id == target_stop_id:
            return offset


def time_delta_from_str(timedelta_string: str) -> timedelta:
    t = datetime.strptime(timedelta_string, "%H:%M:%S")
    delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
    return delta
