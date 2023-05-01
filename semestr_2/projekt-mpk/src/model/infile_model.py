from dataclasses import dataclass, field
from typing import List, Dict


@dataclass(frozen=True)
class Stop:
    id: str = field(hash=True)
    name: str = field(hash=False)
    geolocation: [float] = field(hash=False)
    time_to_other_stops_in_seconds: Dict[str, int] = field(hash=False, default_factory=dict)


@dataclass(frozen=True)
class Route:
    id: str = field(hash=True)
    name: str = field(hash=False)
    stops: List[str] = field(hash=False)


@dataclass(frozen=True)
class Vehicle:
    id: str = field(hash=True)
    capacity: int = field(hash=False)


@dataclass(frozen=True)
class Transit:
    id: str = field(hash=True)
    route_id: str = field(hash=False)
    start_time: str = field(hash=False)
    vehicle_id: str = field(hash=False)
    driver_id: str = field(hash=False)


@dataclass(frozen=True)
class Driver:
    id: str = field(hash=True)
    first_name: str = field(hash=False)
    last_name: str = field(hash=False)
    PESEL: str = field(hash=False)
    phone: str = field(hash=False)


