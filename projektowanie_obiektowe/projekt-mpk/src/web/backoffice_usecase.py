from src.model.internal_model import Driver
from src.repositories.driver_repository import AbstractDriverRepository


def add_driver_usecase(driver_repository: AbstractDriverRepository, name: str, surname: str, pesel: str,
                       phone: str) -> Driver:
    return driver_repository.add(first_name=name, last_name=surname, pesel=pesel, phone=phone)
