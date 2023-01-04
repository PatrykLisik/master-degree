import json
import uuid
from abc import ABC, abstractmethod
from dataclasses import asdict
from typing import Set, Dict, Optional

from sanic.log import logger

from src.model.internal_model import Route
from src.repositories.stop_repository import AbstractStopRepository


class AbstractRouteRepository(ABC):

    @abstractmethod
    def add(self, name: str, stops: list[str]) -> Route:
        raise NotImplementedError

    @abstractmethod
    def update(self, route_id: str, updated_route: Route):
        raise NotImplementedError

    @abstractmethod
    def get(self, route_id: str) -> Route:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> Set[Route]:
        raise NotImplementedError


class InFileRouteRepository(AbstractRouteRepository):
    _file_name = "routes.json"

    def __init__(self, stop_repo: AbstractStopRepository):
        self.stop_repo = stop_repo

    def _get(self) -> Dict[str, Route]:
        try:
            with open(self._file_name, "r+", ) as infile:
                logger.info("load stops")
                data = json.load(infile)
                return {route_data["id"]: Route(
                    **route_data
                )
                    for route_data in data}
        except FileNotFoundError:
            logger.info("file doest not exist")
            return {}

    def _set(self, routes: Dict[str, Route]):
        logger.info("save routes")
        drivers_to_save = [asdict(route) for route in routes.values()]
        json_to_save = json.dumps(drivers_to_save, indent=4)
        with open(self._file_name, "w+") as outfile:
            outfile.write(json_to_save)

    def __int__(self, stop_repo: AbstractStopRepository):
        self.stop_repository = stop_repo

    def add(self, name: str, stops: list[str]) -> Route:
        new_route = Route(name=name, stops=stops, id=str(uuid.uuid4()))
        routes = self._get()
        routes[new_route.id] = new_route
        self._set(routes)
        return new_route

    def update(self, route_id: str, updated_route: Route):
        self._get()[route_id] = updated_route

    def get(self, route_id: str) -> Optional[Route]:
        return self._get().get(route_id, None)

    def get_all(self) -> Set[Route]:
        return set(self._get().values())
