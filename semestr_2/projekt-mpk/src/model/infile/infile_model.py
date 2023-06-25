from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class Stop:
    id: str = field(hash=True)
    name: str = field(hash=False)
    geolocation: [float] = field(hash=False)
    time_to_other_stops_in_seconds: dict[str, int] = field(
        hash=False, default_factory=dict
    )


@dataclass(frozen=True)
class Route:
    id: str = field(hash=True)
    name: str = field(hash=False)
    stops: List[str] = field(hash=False)


@dataclass(frozen=True)
class Transit:
    id: str = field(hash=True)
    route_id: str = field(hash=False)
    start_time: str = field(hash=False)
