from datetime import timedelta

from src.model.domain_model import Stop
from src.repositories.abstract import AbstractStopRepository


async def add_stop_usecase(stop_repository: AbstractStopRepository, name, geo_x, geo_y) -> Stop:
    return stop_repository.add(name=name, geolocation_x=geo_x, geolocation_y=geo_y)


async def get_stop_usecase(stop_repository: AbstractStopRepository, stop_id: str) -> Stop:
    return stop_repository.get(stop_id)


async def get_all_stop_usecase(stop_repository: AbstractStopRepository) -> list[Stop]:
    return [stop for stop in stop_repository.get_all()]


async def get_many_stop_usecase(stop_repository: AbstractStopRepository, stops_ids: set[str]) -> list[Stop]:
    return [stop for stop in stop_repository.get_many(stops_ids)]


async def add_time_between_stops_usecase(stop_repository: AbstractStopRepository, start_stop_id: str, end_stop_id: str,
                                         time_in_sec: int):
    delta_time = timedelta(seconds=time_in_sec)
    stop_repository.set_time_between_stops(start_stop_id, end_stop_id, delta_time)
