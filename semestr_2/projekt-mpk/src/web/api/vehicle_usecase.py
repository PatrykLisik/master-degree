from typing import List

from src.model.domain_model import Vehicle
from src.model.infile_model import Vehicle as InternalVehicle
from src.repositories.abstract import AbstractVehicleRepository


async def add_vehicle_usecase(vehicle_repository: AbstractVehicleRepository, capacity: int) -> Vehicle:
    vehicle = await vehicle_repository.add(capacity=capacity)
    return vehicle


async def get_vehicle_usecase(vehicle_repository: AbstractVehicleRepository, vehicle_id) -> Vehicle:
    return await vehicle_repository.get(vehicle_id)


async def get_all_vehicles_usecase(vehicle_repository: AbstractVehicleRepository) -> List[Vehicle]:
    return [vehicle for vehicle in await vehicle_repository.get_all()]


async def update_vehicle_use_case(vehicle_repository: AbstractVehicleRepository, vehicle_id: str,
                            capacity: int
                            ) -> Vehicle:
    new_vehicle = InternalVehicle(
        capacity=capacity,
        id=vehicle_id
    )
    await vehicle_repository.update(vehicle_id, new_vehicle)
    return new_vehicle
