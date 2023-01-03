import decimal
from dataclasses import dataclass, field
from datetime import timedelta, datetime
from typing import List, Dict


@dataclass(frozen=True)
class Stop:
    id: str = field(hash=True)
    name: str = field(hash=False)
    geolocation: (decimal, decimal) = field(hash=False)
    time_to_other_stops: Dict[str, timedelta] = field(hash=False, default_factory=dict)


@dataclass
class Route:
    name: str
    stops: List[Stop]


@dataclass
class Vehicle:
    id: str
    capacity: int


@dataclass
class Transit:
    route: Route
    start_time: datetime
    vehicle: Vehicle


@dataclass(frozen=True)
class Driver:
    id: str = field(hash=True)
    first_name: str
    last_name: str
    PESEL: str
    phone: str
