from dataclasses import asdict

from sanic import Blueprint, json
from sanic.log import logger

from src.web import route_repository, stop_repository
from src.web.route_usecase import add_route_usecase, get_route_usecase, get_all_routes_usecase

route_blueprint = Blueprint(name="routes")


@route_blueprint.post("/route")
async def add_route(request):
    request_data = request.json
    route = add_route_usecase(
        route_repository=route_repository,
        stop_repository=stop_repository,
        name=request_data.get("name"),
        stops=request_data.get("stops", ""),
    )
    return json(asdict(route))


@route_blueprint.get("/route/<route_id>")
async def get_route(request, route_id):
    route = get_route_usecase(route_repository=route_repository,
                              stop_repository=stop_repository, route_id=route_id)
    logger.info(f"route: {route}")
    return json(asdict(route))


@route_blueprint.get("/routes")
async def get_all_routes(request):
    routes = get_all_routes_usecase(route_repository=route_repository, stop_repository=stop_repository)
    return json(routes)
