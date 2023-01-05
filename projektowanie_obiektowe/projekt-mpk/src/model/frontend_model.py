from dataclasses import dataclass, field
from typing import List, Dict

from src.model.internal_model import Stop as InternalStop, Driver as InternalDriver, Route as InternalRoute
from src.repositories.stop_repository import AbstractStopRepository


@dataclass(frozen=True)
class Stop:
    id: str = field(hash=True)
    name: str = field(hash=False)
    loc_x: str = field(hash=False)
    loc_y: str = field(hash=False)
    time_to_other_stops: Dict[str, str] = field(hash=False, default_factory=dict)

    @classmethod
    def form_internal(cls, stop: InternalStop):
        return cls(
            name=stop.name,
            time_to_other_stops={stop_id: str(time) for stop_id, time in stop.time_to_other_stops.items()},
            loc_x=stop.geolocation[0],
            loc_y=stop.geolocation[1],
            id=stop.id

        )


@dataclass
class Driver:
    first_name: str
    last_name: str
    pesel: str
    phone: str
    id: str

    @classmethod
    def form_internal(cls, driver: InternalDriver):
        return cls(
            first_name=driver.first_name,
            last_name=driver.last_name,
            pesel=driver.PESEL,
            phone=driver.phone,
            id=driver.id
        )


@dataclass
class Route:
    id: str
    name: str
    stops: List[Stop]

    @classmethod
    def form_internal(cls, route: InternalRoute, stops_repository: AbstractStopRepository):
        stop_ids = set(route.stops)
        stops = {stop.id: Stop.form_internal(stop) for stop in stops_repository.get_many(stop_ids)}
        return cls(
            id=route.id,
            name=route.name,
            stops=[stops[stop_id] for stop_id in route.stops]
        )
