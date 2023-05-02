import json
import uuid
from dataclasses import asdict
from typing import Dict, Optional, Set

from sanic.log import logger

from src.model.domain_model import Vehicle as DomainVehicle
from src.model.infile_mappers import infile_vehicle_to_domain
from src.model.infile_model import Vehicle
from src.repositories.abstract import AbstractVehicleRepository


class InMemoryVehicleRepository(AbstractVehicleRepository):

    def __int__(self):
        self._data = {}

    def add(self, capacity: int) -> DomainVehicle:
        new_vehicle = Vehicle(capacity=capacity, id=str(uuid.uuid4()))
        self._data[new_vehicle.id] = new_vehicle
        return infile_vehicle_to_domain(new_vehicle)

    def update(self, vehicle_id: str, updated_vehicle: DomainVehicle):
        self._data[vehicle_id] = Vehicle(capacity=updated_vehicle.capacity, id=updated_vehicle.id)

    def get(self, vehicle_id: str) -> DomainVehicle:
        return infile_vehicle_to_domain(self._data[vehicle_id])

    def get_all(self) -> Set[DomainVehicle]:
        return {infile_vehicle_to_domain(vehicle) for vehicle in self._data.values()}


class InFileVehicleRepository(AbstractVehicleRepository):
    _file_name = "data/vehicles.json"

    def _get(self) -> Dict[str, Vehicle]:
        try:
            with open(self._file_name, "r+", ) as infile:
                logger.info("load vehicles")
                data = json.load(infile)
                return {vehicle_data["id"]: Vehicle(
                    **vehicle_data
                )
                    for vehicle_data in data}
        except FileNotFoundError:
            logger.info("load vehicle file doest not exist")
            return {}

    def _set(self, vehicles: Dict[str, Vehicle]):
        logger.info("save vehicles")
        vehicles_to_save = [asdict(vehicle) for vehicle in vehicles.values()]
        json_to_save = json.dumps(vehicles_to_save, indent=4)
        with open(self._file_name, "w+") as outfile:
            outfile.write(json_to_save)

    def add(self, capacity: int) -> DomainVehicle:
        new_vehicle = Vehicle(capacity=capacity, id=str(uuid.uuid4()))
        vehicles = self._get()
        vehicles[new_vehicle.id] = new_vehicle
        self._set(vehicles)
        return new_vehicle

    def update(self, vehicle_id: str, updated_vehicle: DomainVehicle):
        vehicles = self._get()
        vehicles[updated_vehicle.id] = Vehicle(id=updated_vehicle.id, capacity=updated_vehicle.capacity)
        self._set(vehicles)

    def get(self, vehicle_id: str) -> Optional[DomainVehicle]:
        vehicle = self._get()[vehicle_id]
        return infile_vehicle_to_domain(vehicle)

    def get_all(self) -> set[DomainVehicle]:
        return {infile_vehicle_to_domain(vehicle) for vehicle in self._get().values()}
