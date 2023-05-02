import json as jjson
from dataclasses import asdict

from sanic import Blueprint, HTTPResponse, json, Request
from sanic.log import logger

from src.repositories.abstract import AbstractRouteRepository
from src.web.api.route_usecase import (
    add_route_usecase,
    get_all_routes_usecase,
    get_route_usecase,
)

route_blueprint = Blueprint(name="routes")


@route_blueprint.post("/route")
async def add_route(
    request: Request, route_repository: AbstractRouteRepository
) -> HTTPResponse:
    request_data = request.json
    route = await add_route_usecase(
        route_repository=route_repository,
        name=request_data.get("name"),
        stops=request_data.get("stops", ""),
    )
    return json(asdict(route))


@route_blueprint.get("/route/<route_id>")
async def get_route(
    request: Request, route_id, route_repository: AbstractRouteRepository
) -> HTTPResponse:
    route = await get_route_usecase(
        route_repository=route_repository, route_id=route_id
    )
    logger.info(f"route: {route}")
    return json(asdict(route), dumps=jjson.dumps, default=str)


@route_blueprint.get("/routes")
async def get_all_routes(
    request: Request, route_repository: AbstractRouteRepository
) -> HTTPResponse:
    routes = await get_all_routes_usecase(route_repository=route_repository)
    return json([asdict(route) for route in routes])
