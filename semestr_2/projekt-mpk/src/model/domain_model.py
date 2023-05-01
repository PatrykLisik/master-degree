from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List


@dataclass(frozen=True)
class Stop:
    id: str = field(hash=True)
    name: str = field(hash=False)
    loc_x: str = field(hash=False)
    loc_y: str = field(hash=False)
    time_to_other_stops: Dict[str, timedelta] = field(hash=False, default_factory=dict)


@dataclass
class Driver:
    first_name: str
    last_name: str
    pesel: str
    phone: str
    id: str


@dataclass(frozen=True)
class Route:
    id: str = field(hash=True)
    name: str = field(hash=True)
    stops: List[Stop] = field(hash=False)


@dataclass
class Vehicle:
    id: str
    capacity: int


@dataclass
class Transit:
    id:str
    route: Route
    start_time: datetime
    vehicle: Vehicle
    driver: Driver


class UserType(Enum):
    App = 1
    Backoffice = 2


@dataclass(frozen=True)
class User:
    id: str
    name: str
    email: str
    password_hash: str
    user_type: UserType
