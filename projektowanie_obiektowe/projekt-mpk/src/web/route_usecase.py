from typing import List, Set

from src.model.frontend_model import Route
from src.repositories.route_repository import AbstractRouteRepository
from src.repositories.stop_repository import AbstractStopRepository


def add_route_usecase(route_repository: AbstractRouteRepository, stop_repository: AbstractStopRepository, name: str,
                      stops: List[str]) -> Route:
    route = route_repository.add(name, stops)
    return Route.from_internal(route, stop_repository)


def get_all_routes_usecase(route_repository: AbstractRouteRepository, stop_repository: AbstractStopRepository) -> Set[
    Route]:
    return {Route.from_internal(route=route, stops_repository=stop_repository) for route in route_repository.get_all()}


def get_route_usecase(route_repository: AbstractRouteRepository, stop_repository: AbstractStopRepository,
                      route_id: str) -> Route:
    return Route.from_internal(route_repository.get(route_id), stop_repository)
