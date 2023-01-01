from dataclasses import dataclass
from typing import List, Dict, Self
from datetime import timedelta, datetime


@dataclass
class Stop:
    id: str
    name: str
    geolocation: (float, float)
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


@dataclass
class Driver:
    id: str
    first_name: str
    last_name: str
    PESEL: str
    phone: str
