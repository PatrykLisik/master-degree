import datetime
from typing import List

from src.model.domain_model import Transit
from src.repositories.abstract import AbstractTransitRepository


async def add_transit_usecase(
    transit_repository: AbstractTransitRepository,
    route_id: str,
    start_time: datetime,
    vehicle_id: str,
    driver_id: str,
) -> Transit:
    transit = await transit_repository.add(route_id, start_time, vehicle_id, driver_id)
    return transit


async def get_transit_usecase(
    transit_repository: AbstractTransitRepository, transit_id
) -> Transit:
    return await transit_repository.get(transit_id)


async def get_all_transits_usecase(
    transit_repository: AbstractTransitRepository,
) -> List[Transit]:
    return list(await transit_repository.get_all())
