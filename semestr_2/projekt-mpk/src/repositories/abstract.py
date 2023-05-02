import decimal
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Set

from src.model.domain_model import (
    Driver as DomainDriver,
    Route as DomainRoute,
    Stop as DomainStop,
    Transit as DomainTransit,
    User,
    UserType,
    Vehicle as DomainVehicle
)


class AbstractDriverRepository(ABC):

    @abstractmethod
    async def add(self, first_name: str, last_name: str, pesel: str, phone: str) -> DomainDriver:
        raise NotImplementedError

    @abstractmethod
    async def update(self, driver_id: str, updated_driver: DomainDriver):
        raise NotImplementedError

    @abstractmethod
    async def get(self, driver_id: str) -> DomainDriver:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> Set[DomainDriver]:
        raise NotImplementedError


class AbstractRouteRepository(ABC):

    @abstractmethod
    async def add(self, name: str, stops: list[str]) -> DomainRoute:
        raise NotImplementedError

    @abstractmethod
    async def update(self, route_id: str, updated_route: DomainRoute):
        raise NotImplementedError

    @abstractmethod
    async def get(self, route_id: str) -> DomainRoute:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> Set[DomainRoute]:
        raise NotImplementedError


class AbstractStopRepository(ABC):

    @abstractmethod
    async def add(self, name: str, geolocation_x: decimal, geolocation_y: decimal) -> DomainStop:
        raise NotImplementedError

    @abstractmethod
    async def update(self, stop_id: str, updated_stop: DomainStop):
        raise NotImplementedError

    @abstractmethod
    async def get(self, stop_id: str) -> DomainStop:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> Set[DomainStop]:
        raise NotImplementedError

    @abstractmethod
    async def get_many(self, stop_ids: set[str]) -> Set[DomainStop]:
        raise NotImplementedError

    @abstractmethod
    async def set_time_between_stops(self, start_stop_id: str, end_stop_id: str, time: timedelta):
        raise NotImplementedError


class AbstractTransitRepository(ABC):

    @abstractmethod
    async def add(self,
            route_id: str,
            start_time: datetime,
            vehicle_id: str,
            driver_id: str) -> DomainTransit:
        raise NotImplementedError

    @abstractmethod
    async def update(self, transit_id: str, updated_transit: DomainTransit):
        raise NotImplementedError

    @abstractmethod
    async def get(self, transit_id: str) -> DomainTransit:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> Set[DomainTransit]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_route(self, route_id: str) -> Set[DomainTransit]:
        raise NotImplementedError


class AbstractUserRepository(ABC):

    @abstractmethod
    async def add(self, name: str, email: str, password_hash: str, user_type: UserType) -> User:
        raise NotImplementedError

    @abstractmethod
    async def login(self, email: str, password_hash: str, ) -> User:
        raise NotImplementedError


class AbstractVehicleRepository(ABC):

    @abstractmethod
    async def add(self, capacity: int) -> DomainVehicle:
        raise NotImplementedError

    @abstractmethod
    async def update(self, vehicle_id: str, updated_vehicle: DomainVehicle):
        raise NotImplementedError

    @abstractmethod
    async def get(self, vehicle_id: str) -> DomainVehicle:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> Set[DomainVehicle]:
        raise NotImplementedError
