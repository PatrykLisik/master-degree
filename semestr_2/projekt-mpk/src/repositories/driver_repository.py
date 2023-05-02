import json
import uuid
from dataclasses import asdict
from typing import Dict, Optional, Set

from sanic.log import logger
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.model.domain_model import Driver as DomainDriver
from src.model.infile_mappers import infile_driver_to_domain
from src.model.infile_model import Driver as InFileDriver
from src.repositories.abstract import AbstractDriverRepository
from src.model.database.model import Driver as DBDriver


class InMemoryDriverRepository(AbstractDriverRepository):
    _data: Dict[str, InFileDriver] = {}

    def add(self, first_name: str, last_name: str, pesel: str, phone: str) -> DomainDriver:
        new_driver = InFileDriver(first_name=first_name, last_name=last_name, PESEL=pesel, phone=phone,
                                  id=str(uuid.uuid4()))
        self._data[new_driver.id] = new_driver
        return infile_driver_to_domain(new_driver)

    def update(self, driver_id: str, updated_driver: DomainDriver):
        self._data[driver_id] = updated_driver

    def get(self, driver_id: str) -> Optional[DomainDriver]:
        infile_driver = self._data.get(driver_id, None)
        if infile_driver is None:
            return None
        return infile_driver_to_domain(infile_driver)

    def get_all(self) -> Set[DomainDriver]:
        return {infile_driver_to_domain(infile_driver) for infile_driver in self._data.values()}


class InFileDriverRepository(AbstractDriverRepository):
    _file_name = "data/drivers.json"

    def _get(self) -> Dict[str, InFileDriver]:
        try:
            with open(self._file_name, "r+", ) as infile:
                logger.info("load driver")
                data = json.load(infile)
                return {driver_data["id"]: InFileDriver(
                    **driver_data
                )
                    for driver_data in data}
        except FileNotFoundError:
            logger.info("load driver file doest not exist")
            return {}

    def _set(self, drivers: Dict[str, InFileDriver]):
        logger.info("save drivers")
        drivers_to_save = [asdict(driver) for driver in drivers.values()]
        json_to_save = json.dumps(drivers_to_save, indent=4)
        with open(self._file_name, "w+") as outfile:
            outfile.write(json_to_save)

    async def add(self, first_name: str, last_name: str, pesel: str, phone: str) -> DomainDriver:
        new_driver = InFileDriver(first_name=first_name, last_name=last_name, PESEL=pesel, phone=phone, id=str(uuid.uuid4()))
        drivers = self._get()
        drivers[new_driver.id] = new_driver
        self._set(drivers)
        return new_driver

    async def update(self, driver_id: str, updated_driver: DomainDriver):
        drivers = self._get()
        drivers[updated_driver.id] = updated_driver
        self._set(drivers)

    async def get(self, driver_id: str) -> Optional[DomainDriver]:
        drivers = self._get()
        return drivers.get(driver_id, None)

    async def get_all(self) -> Set[DomainDriver]:
        return {infile_driver_to_domain(infile_driver) for infile_driver in self._get().values()}


class DatabaseDriverRepository(AbstractDriverRepository):

    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        self.session_maker = session_maker

    async def add(self, first_name: str, last_name: str, pesel: str, phone: str) -> DomainDriver:
        async with self.session_maker() as session:
            async with session.begin():
                new_driver = DBDriver(
                    first_name=first_name,
                    last_name=last_name,
                    pesel=pesel,
                    phone=phone
                )
                session.add(new_driver)
                await session.flush()
                return DomainDriver(
                    id=new_driver.id,
                    first_name=first_name,
                    last_name=last_name,
                    pesel=pesel,
                    phone=phone
                )

    async def update(self, driver_id: str, updated_driver: DomainDriver):
        pass

    async def get(self, driver_id: str) -> DomainDriver:
        pass

    async def get_all(self) -> Set[DomainDriver]:
        pass