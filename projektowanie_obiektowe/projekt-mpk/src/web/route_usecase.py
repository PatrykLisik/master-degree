from typing import List

from src.model.frontend_model import Route
from src.repositories.route_repository import AbstractRouteRepository
from src.repositories.stop_repository import AbstractStopRepository


def add_route(repository: AbstractRouteRepository, stops_repository: AbstractStopRepository, name: str,
              stops: List[str]) -> Route:
    route = repository.add(name, stops)
    return Route.form_internal(route, stops_repository)


def get_all_routes(route_repository: AbstractRouteRepository, stops_repository: AbstractStopRepository) -> List[Route]:
    return [Route.form_internal(route, stops_repository) for route in route_repository.get_all()]


def get_route(route_repository: AbstractRouteRepository, stops_repository: AbstractStopRepository,
              route_id: str) -> Route:
    return Route.form_internal(route_repository.get(route_id), stops_repository)
