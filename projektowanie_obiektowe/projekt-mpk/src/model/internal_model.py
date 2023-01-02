import decimal
from dataclasses import dataclass, field
from datetime import timedelta, datetime
from typing import List, Dict, Self


@dataclass(frozen=True)
class Stop:
    id: str = field(hash=True)
    name: str
    geolocation: (decimal, decimal)
    time_to_other_stops: Dict[Self, timedelta]


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
