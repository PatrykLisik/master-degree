from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum


@dataclass(frozen=True)
class Stop:
    id: str = field(hash=True)
    name: str = field(hash=False)
    loc_x: str = field(hash=False)
    loc_y: str = field(hash=False)
    time_to_other_stops: dict[str, timedelta] = field(hash=False, default_factory=dict)


@dataclass(frozen=True)
class Driver:
    first_name: str = field(hash=False)
    last_name: str = field(hash=False)
    pesel: str = field(hash=False)
    phone: str = field(hash=False)
    id: str = field(hash=True)


@dataclass(frozen=True)
class Route:
    id: str = field(hash=True)
    name: str = field(hash=True)
    stops: list[Stop] = field(hash=False)


@dataclass(frozen=True)
class Vehicle:
    id: str = field(hash=True)
    capacity: int = field(hash=False)


@dataclass(frozen=True)
class Transit:
    id: str = field(hash=True)
    route: Route = field(hash=False)
    start_time: datetime = field(hash=False)
    vehicle: Vehicle = field(hash=False)
    driver: Driver = field(hash=False)


class UserType(Enum):
    App = 1
    Backoffice = 2


@dataclass(frozen=True)
class User:
    id: str = field(hash=True)
    name: str = field(hash=False)
    email: str = field(hash=False)
    password_hash: str = field(hash=False)
    user_type: UserType = field(hash=False)
