from src.model.internal_model import Stop
from src.repositories.stop_repository import AbstractStopRepository


async def add_stop_usecase(stop_repository: AbstractStopRepository, name, geo_x, geo_y) -> Stop:
    return await stop_repository.add(name=name, geolocation_x=geo_x, geolocation_y=geo_y)
