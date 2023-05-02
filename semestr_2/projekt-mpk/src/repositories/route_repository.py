import json
import uuid
from dataclasses import asdict
from typing import Dict, Optional, Set

from sanic.log import logger

from src.model.domain_model import Route as DomainRoute
from src.model.infile_mappers import domain_route_to_infile, infile_route_to_domain
from src.model.infile_model import Route
from src.repositories.abstract import AbstractRouteRepository, AbstractStopRepository


class InFileRouteRepository(AbstractRouteRepository):
    _file_name = "data/routes.json"

    def __init__(self, stops_repository: AbstractStopRepository):
        super()
        self.stops_repository = stops_repository

    def _get(self) -> Dict[str, Route]:
        try:
            with open(self._file_name, "r+", ) as infile:
                logger.info("load routes")
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

    def add(self, name: str, stops: list[str]) -> DomainRoute:
        new_route = Route(name=name, stops=stops, id=str(uuid.uuid4()))
        routes = self._get()
        routes[new_route.id] = new_route
        self._set(routes)
        return infile_route_to_domain(new_route, self.stops_repository)

    def update(self, route_id: str, updated_route: DomainRoute):
        self._get()[route_id] = domain_route_to_infile(updated_route)

    def get(self, route_id: str) -> Optional[DomainRoute]:
        route = self._get().get(route_id, None)
        if route is None:
            return None
        return infile_route_to_domain(route, self.stops_repository)

    def get_all(self) -> Set[DomainRoute]:
        return {infile_route_to_domain(route, self.stops_repository) for route in self._get().values()}
