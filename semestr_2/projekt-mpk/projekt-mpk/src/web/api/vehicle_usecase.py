from typing import List

from src.model.frontend_model import Vehicle
from src.model.internal_model import Vehicle as InternalVehicle
from src.repositories.vehicle_repository import AbstractVehicleRepository


def add_vehicle_usecase(vehicle_repository: AbstractVehicleRepository, capacity: int) -> Vehicle:
    vehicle = vehicle_repository.add(capacity=capacity)
    return Vehicle.form_internal(vehicle)


def get_vehicle_usecase(vehicle_repository: AbstractVehicleRepository, vehicle_id) -> Vehicle:
    return Vehicle.form_internal(vehicle_repository.get(vehicle_id))


def get_all_vehicles_usecase(vehicle_repository: AbstractVehicleRepository) -> List[Vehicle]:
    return [Vehicle.form_internal(vehicle) for vehicle in vehicle_repository.get_all()]


def update_vehicle_use_case(vehicle_repository: AbstractVehicleRepository, vehicle_id: str,
                            capacity: int
                            ) -> Vehicle:
    new_vehicle = InternalVehicle(
        capacity=capacity,
        id=vehicle_id
    )
    vehicle_repository.update(vehicle_id, new_vehicle)
    return Vehicle.form_internal(new_vehicle)
