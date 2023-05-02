from typing import List, Set

from src.model.domain_model import Route
from src.repositories.abstract import AbstractRouteRepository


async def add_route_usecase(route_repository: AbstractRouteRepository, name: str,
                            stops: List[str]) -> Route:
    route = route_repository.add(name, stops)
    return await route


async def get_all_routes_usecase(route_repository: AbstractRouteRepository) -> Set[Route]:
    return await route_repository.get_all()


async def get_route_usecase(route_repository: AbstractRouteRepository,
                            route_id: str) -> Route:
    return await route_repository.get(route_id)
