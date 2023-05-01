from typing import Optional, List

from src.model.domain_model import Driver
from src.model.infile_model import Driver as InternalDriver
from src.repositories.abstract import AbstractDriverRepository


def add_driver_usecase(driver_repository: AbstractDriverRepository, name: str, surname: str, pesel: str,
                       phone: str) -> Driver:
    driver = driver_repository.add(first_name=name, last_name=surname, pesel=pesel, phone=phone)
    return Driver.form_internal(driver)


def get_driver_usecase(driver_repository: AbstractDriverRepository, driver_id) -> Driver:
    return Driver.form_internal(driver_repository.get(driver_id))


def get_all_drivers_usecase(driver_repository: AbstractDriverRepository) -> List[Driver]:
    return [Driver.form_internal(driver) for driver in driver_repository.get_all()]


def update_driver_use_case(driver_repository: AbstractDriverRepository, name: Optional[str], surname: Optional[str],
                           pesel: Optional[str], driver_id: str,
                           phone: Optional[str]
                           ) -> Driver:
    old_driver = driver_repository.get(driver_id)
    new_driver = InternalDriver(
        first_name=name or old_driver.first_name,
        last_name=surname or old_driver.last_name,
        phone=phone or old_driver.phone,
        PESEL=pesel or old_driver.PESEL,
        id=driver_id
    )
    driver_repository.update(driver_id, new_driver)
    return Driver.form_internal(new_driver)
