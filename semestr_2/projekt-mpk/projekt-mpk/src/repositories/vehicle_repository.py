import json
import uuid
from abc import ABC, abstractmethod
from dataclasses import asdict
from typing import Set, Dict, Optional

from sanic.log import logger

from src.model.internal_model import Vehicle


class AbstractVehicleRepository(ABC):

    @abstractmethod
    def add(self, capacity: int) -> Vehicle:
        raise NotImplementedError

    @abstractmethod
    def update(self, vehicle_id: str, updated_vehicle: Vehicle):
        raise NotImplementedError

    @abstractmethod
    def get(self, vehicle_id: str) -> Vehicle:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> Set[Vehicle]:
        raise NotImplementedError


class InMemoryVehicleRepository(AbstractVehicleRepository):

    def __int__(self):
        self._data = {}

    def add(self, capacity: int) -> Vehicle:
        new_vehicle = Vehicle(capacity=capacity, id=str(uuid.uuid4()))
        self._data[new_vehicle.id] = new_vehicle
        return new_vehicle

    def update(self, vehicle_id: str, updated_vehicle: Vehicle):
        self._data[vehicle_id] = updated_vehicle

    def get(self, vehicle_id: str) -> Vehicle:
        return self._data[vehicle_id]

    def get_all(self) -> Set[Vehicle]:
        return set(self._data.values())


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

    def add(self, capacity: int) -> Vehicle:
        new_vehicle = Vehicle(capacity=capacity, id=str(uuid.uuid4()))
        vehicles = self._get()
        vehicles[new_vehicle.id] = new_vehicle
        self._set(vehicles)
        return new_vehicle

    def update(self, vehicle_id: str, updated_vehicle: Vehicle):
        vehicles = self._get()
        vehicles[updated_vehicle.id] = updated_vehicle
        self._set(vehicles)

    def get(self, vehicle_id: str) -> Optional[Vehicle]:
        vehicles = self._get()
        return vehicles.get(vehicle_id, None)

    def get_all(self) -> Set[Vehicle]:
        return set(self._get().values())
