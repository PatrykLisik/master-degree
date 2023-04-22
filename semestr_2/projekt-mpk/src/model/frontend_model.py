from dataclasses import dataclass, field
from typing import List, Dict

from src.model.internal_model import Stop as InternalStop, Driver as InternalDriver, Route as InternalRoute, \
    Transit as InternalTransit, Vehicle as InternalVehicle
from src.repositories.driver_repository import AbstractDriverRepository
from src.repositories.route_repository import AbstractRouteRepository
from src.repositories.stop_repository import AbstractStopRepository
from src.repositories.vehicle_repository import AbstractVehicleRepository


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


@dataclass(frozen=True)
class Route:
    id: str = field(hash=True)
    name: str = field(hash=True)
    stops: List[Stop] = field(hash=False)

    @classmethod
    def from_internal(cls, route: InternalRoute, stops_repository: AbstractStopRepository):
        stop_ids = set(route.stops)
        stops = {stop.id: Stop.form_internal(stop) for stop in stops_repository.get_many(stop_ids)}
        return cls(
            id=route.id,
            name=route.name,
            stops=[stops[stop_id] for stop_id in route.stops]
        )


@dataclass
class Vehicle:
    id: str
    capacity: int

    @classmethod
    def form_internal(cls, vehicle: InternalVehicle):
        return Vehicle(
            id=vehicle.id,
            capacity=vehicle.capacity
        )


@dataclass
class Transit:
    route: Route
    start_time: str
    vehicle: Vehicle
    driver: Driver

    @classmethod
    def form_internal(cls, transit: InternalTransit,
                      stops_repo: AbstractStopRepository,
                      route_repo: AbstractRouteRepository,
                      driver_repo: AbstractDriverRepository,
                      vehicle_repo: AbstractVehicleRepository
                      ):
        route = Route.from_internal(route=route_repo.get(transit.route_id), stops_repository=stops_repo)
        return Transit(
            route=route,
            start_time=str(transit.start_time),
            vehicle=Vehicle.form_internal(vehicle=vehicle_repo.get(transit.vehicle_id)),
            driver=Driver.form_internal(driver_repo.get(transit.driver_id))
        )
