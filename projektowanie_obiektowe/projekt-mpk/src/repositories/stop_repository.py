import decimal
import uuid
from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Set, Dict, Optional

from src.model.internal_model import Stop


class AbstractStopRepository(ABC):

    @abstractmethod
    def add(self,
            name: str,
            location: (decimal, decimal),
            time_to_other_stops: Optional[Dict[Stop, timedelta]] = None) -> Stop:
        raise NotImplementedError

    @abstractmethod
    def update(self, driver_id: str, updated_driver: Stop):
        raise NotImplementedError

    @abstractmethod
    def get(self, driver_id: str) -> Stop:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> Set[Stop]:
        raise NotImplementedError


class FakeStopRepository(AbstractStopRepository):

    def __int__(self):
        self._data = {}

    def add(self, first_name: str, last_name: str, pesel: str, phone: str) -> Stop:
        new_driver = Stop(first_name=first_name, last_name=last_name, PESEL=pesel, phone=phone, id=str(uuid.uuid4()))
        self._data[new_driver.id] = new_driver
        return new_driver

    def update(self, driver_id: str, updated_driver: Stop):
        self._data[driver_id] = updated_driver

    def get(self, driver_id: str) -> Stop:
        return self._data[driver_id]

    def get_all(self) -> Set[Stop]:
        return set(self._data.values())
