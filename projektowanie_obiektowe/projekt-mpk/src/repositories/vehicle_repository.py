import uuid
from abc import ABC, abstractmethod
from typing import Set

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


class FakeVehicleRepository(AbstractVehicleRepository):

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
