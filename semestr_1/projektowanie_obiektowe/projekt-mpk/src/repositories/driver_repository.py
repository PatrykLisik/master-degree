import json
import uuid
from abc import ABC, abstractmethod
from dataclasses import asdict
from typing import Set, Dict, Optional

from sanic.log import logger

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


class InFileDriverRepository(AbstractDriverRepository):
    _file_name = "data/drivers.json"

    def _get(self) -> Dict[str, Driver]:
        try:
            with open(self._file_name, "r+", ) as infile:
                logger.info("load driver")
                data = json.load(infile)
                return {driver_data["id"]: Driver(
                    **driver_data
                )
                    for driver_data in data}
        except FileNotFoundError:
            logger.info("load driver file doest not exist")
            return {}

    def _set(self, drivers: Dict[str, Driver]):
        logger.info("save drivers")
        drivers_to_save = [asdict(driver) for driver in drivers.values()]
        json_to_save = json.dumps(drivers_to_save, indent=4)
        with open(self._file_name, "w+") as outfile:
            outfile.write(json_to_save)

    def add(self, first_name: str, last_name: str, pesel: str, phone: str) -> Driver:
        new_driver = Driver(first_name=first_name, last_name=last_name, PESEL=pesel, phone=phone, id=str(uuid.uuid4()))
        drivers = self._get()
        drivers[new_driver.id] = new_driver
        self._set(drivers)
        return new_driver

    def update(self, driver_id: str, updated_driver: Driver):
        drivers = self._get()
        drivers[updated_driver.id] = updated_driver
        self._set(drivers)

    def get(self, driver_id: str) -> Optional[Driver]:
        drivers = self._get()
        return drivers.get(driver_id, None)

    def get_all(self) -> Set[Driver]:
        return set(self._get().values())
