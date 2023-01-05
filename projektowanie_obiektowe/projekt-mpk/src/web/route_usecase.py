from typing import List

from src.model.frontend_model import Route
from src.repositories.route_repository import AbstractRouteRepository
from src.repositories.stop_repository import AbstractStopRepository


def add_route_usecase(route_repository: AbstractRouteRepository, stop_repository: AbstractStopRepository, name: str,
                      stops: List[str]) -> Route:
    route = route_repository.add(name, stops)
    return Route.form_internal(route, stop_repository)


def get_all_routes_usecase(route_repository: AbstractRouteRepository) -> dict[
    str, str]:
    return {route.id: route.name for route in route_repository.get_all()}


def get_route_usecase(route_repository: AbstractRouteRepository, stop_repository: AbstractStopRepository,
                      route_id: str) -> Route:
    return Route.form_internal(route_repository.get(route_id), stop_repository)
