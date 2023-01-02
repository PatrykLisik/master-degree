import uuid
from abc import ABC, abstractmethod
from typing import Set, Dict, Optional

from src.model.internal_model import Driver


class AbstractDriverRepository(ABC):

    @abstractmethod
    def add(self, first_name: str, last_name: str, pesel: str, phone: str) -> Driver:
        raise NotImplementedError

    @abstractmethod
    def update(self, driver_id: str, updated_driver: Driver):
        raise NotImplementedError

    @abstractmethod
    def get(self, driver_id: str) -> Driver:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> Set[Driver]:
        raise NotImplementedError


class InMemoryDriverRepository(AbstractDriverRepository):
    _data: Dict[str, Driver] = {}

    def add(self, first_name: str, last_name: str, pesel: str, phone: str) -> Driver:
        new_driver = Driver(first_name=first_name, last_name=last_name, PESEL=pesel, phone=phone, id=str(uuid.uuid4()))
        self._data[new_driver.id] = new_driver
        return new_driver

    def update(self, driver_id: str, updated_driver: Driver):
        self._data[driver_id] = updated_driver

    def get(self, driver_id: str) -> Optional[Driver]:
        return self._data.get(driver_id, None)

    def get_all(self) -> Set[Driver]:
        return set(self._data.values())
