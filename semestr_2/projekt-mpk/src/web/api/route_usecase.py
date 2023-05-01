from typing import List, Set

from src.model.domain_model import Route
from src.repositories.abstract import AbstractRouteRepository, AbstractStopRepository


def add_route_usecase(route_repository: AbstractRouteRepository, name: str,
                      stops: List[str]) -> Route:
    route = route_repository.add(name, stops)
    return route


def get_all_routes_usecase(route_repository: AbstractRouteRepository, stop_repository: AbstractStopRepository) -> Set[
    Route]:
    return route_repository.get_all()


def get_route_usecase(route_repository: AbstractRouteRepository,
                      route_id: str) -> Route:
    return route_repository.get(route_id)
