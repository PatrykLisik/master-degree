from dataclasses import dataclass


@dataclass
class DriverCreateModel:
    first_name: str
    last_name: str
    PESEL: str
    phone: str
