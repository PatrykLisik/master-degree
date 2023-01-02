from typing import Set, Optional

from src.model.internal_model import Driver
from src.repositories.driver_repository import AbstractDriverRepository


def add_driver_usecase(driver_repository: AbstractDriverRepository, name: str, surname: str, pesel: str,
                       phone: str) -> Driver:
    return driver_repository.add(first_name=name, last_name=surname, pesel=pesel, phone=phone)


def get_driver_usecase(driver_repository: AbstractDriverRepository, driver_id) -> Driver:
    return driver_repository.get(driver_id)


def get_all_drivers_usecase(driver_repository: AbstractDriverRepository) -> Set[Driver]:
    return driver_repository.get_all()


def update_driver_use_case(driver_repository: AbstractDriverRepository, name: Optional[str], surname: Optional[str],
                           pesel: Optional[str], driver_id: str,
                           phone: Optional[str]

                           ) -> Driver:
    old_driver = driver_repository.get(driver_id)
    new_driver = Driver(
        first_name=name or old_driver.first_name,
        last_name=surname or old_driver.last_name,
        phone=phone or old_driver.phone,
        PESEL=pesel or old_driver.PESEL,
        id=driver_id
    )
    driver_repository.update(driver_id, new_driver)
    return new_driver
