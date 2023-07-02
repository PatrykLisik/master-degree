import decimal
from abc import ABC, abstractmethod
from datetime import timedelta, time
from typing import Set

from src.model.domain_model import (
    Route as DomainRoute,
    Stop as DomainStop,
    Transit as DomainTransit,
    User,
    UserType,
)


class AbstractRouteRepository(ABC):
    @abstractmethod
    async def add(self, name: str) -> DomainRoute:
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

    @abstractmethod
    async def search_by_name(self, query: str) -> Set[DomainRoute]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, route_id: str):
        pass


class AbstractStopRepository(ABC):
    @abstractmethod
    async def add(
        self, name: str, geolocation_x: decimal, geolocation_y: decimal
    ) -> DomainStop:
        raise NotImplementedError

    @abstractmethod
    async def update(self, stop_id: str, updated_stop: DomainStop):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, stop_id: str):
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
    async def set_time_between_stops(
        self, start_stop_id: str, end_stop_id: str, time: timedelta
    ):
        raise NotImplementedError

    @abstractmethod
    async def delete_time_between_stops(self, start_stop_id: str, end_stop_id: str):
        raise NotImplementedError

    @abstractmethod
    async def search_by_name(self, query) -> Set[DomainStop]:
        raise NotImplementedError


class AbstractTransitRepository(ABC):
    @abstractmethod
    async def add(
        self,
        route_id: str,
        start_time: time,
    ) -> DomainTransit:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, transit_id: str):
        raise NotImplementedError


class AbstractUserRepository(ABC):
    @abstractmethod
    async def add(
        self, name: str, email: str, password_hash: str, user_type: UserType
    ) -> User:
        raise NotImplementedError

    @abstractmethod
    async def login(
        self,
        email: str,
        password_hash: str,
    ) -> User:
        raise NotImplementedError
