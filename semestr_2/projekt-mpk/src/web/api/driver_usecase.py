from typing import List, Optional

from src.model.domain_model import Driver
from src.model.infile_model import Driver as InternalDriver
from src.repositories.abstract import AbstractDriverRepository


async def add_driver_usecase(driver_repository: AbstractDriverRepository, name: str, surname: str, pesel: str,
                             phone: str) -> Driver:
    driver = await driver_repository.add(first_name=name, last_name=surname, pesel=pesel, phone=phone)
    return driver


async def get_driver_usecase(driver_repository: AbstractDriverRepository, driver_id) -> Driver:
    return await driver_repository.get(driver_id)


async def get_all_drivers_usecase(driver_repository: AbstractDriverRepository) -> List[Driver]:
    return [driver for driver in await driver_repository.get_all()]


async def update_driver_use_case(driver_repository: AbstractDriverRepository, name: Optional[str],
                                 surname: Optional[str],
                                 pesel: Optional[str], driver_id: str,
                                 phone: Optional[str]
                                 ) -> Driver:
    old_driver = await driver_repository.get(driver_id)
    new_driver = InternalDriver(
        first_name=name or old_driver.first_name,
        last_name=surname or old_driver.last_name,
        phone=phone or old_driver.phone,
        PESEL=pesel or old_driver.pesel,
        id=driver_id
    )
    await driver_repository.update(driver_id, new_driver)
    return new_driver
