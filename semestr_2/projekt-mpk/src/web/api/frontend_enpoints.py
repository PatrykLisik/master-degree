from __future__ import annotations

import json

from sanic import Blueprint, HTTPResponse, Request
from sanic.log import logger
from sanic_ext import render

from src.repositories.abstract import AbstractRouteRepository, AbstractTransitRepository
from src.web.api import COOKIE_KEY
from src.web.api.mobile_app_usecase import get_all_routes_usecase, get_route_stops_usecase, get_stop_timetable_usecase

html_blueprint = Blueprint(name="frontend", url_prefix="/")


@html_blueprint.get("/")
async def index(request: Request,
                route_repository: AbstractRouteRepository,
                ) -> HTTPResponse:
    user_data = request.cookies.get(COOKIE_KEY, {})
    if user_data:
        user_data = json.loads(user_data)
    logger.debug(f"Cookie {user_data}")

    routes = await get_all_routes_usecase(route_repository)
    logger.debug(f"Routes: {routes}")
    return await render(
        "browse_lines.html", status=200, context={"user_data": user_data, "routes": routes, "current_route": None}
    )


@html_blueprint.get("/<route_id>/")
async def index_with_route(request: Request,
                           route_id: str | None,
                           route_repository: AbstractRouteRepository,
                           ) -> HTTPResponse:
    user_data = request.cookies.get(COOKIE_KEY, {})
    if user_data:
        user_data = json.loads(user_data)
    logger.debug(f"Cookie {user_data}")

    routes = await get_all_routes_usecase(route_repository)
    logger.debug(f"Routes: {routes}")

    stops = await get_route_stops_usecase(
        route_repository=route_repository, route_id=route_id
    )

    return await render(
        "browse_lines.html", status=200, context={"user_data": user_data,
                                                  "routes": routes,
                                                  "current_route": route_id,
                                                  "stops": stops
                                                  }
    )


@html_blueprint.get("/<route_id>/<stop_id>/")
async def index_with_route_and_stop_selected(request: Request,
                                             route_id: str | None,
                                             stop_id: str | None,
                                             route_repository: AbstractRouteRepository,
                                             transit_repository: AbstractTransitRepository,
                                             ) -> HTTPResponse:
    if not route_id or not stop_id:
        return HTTPResponse(status=418)
    user_data = request.cookies.get(COOKIE_KEY, {})
    if user_data:
        user_data = json.loads(user_data)
    logger.debug(f"Cookie {user_data}")

    routes = await get_all_routes_usecase(route_repository)

    time_table = None
    if route_id and stop_id:
        time_table = await get_stop_timetable_usecase(
            route_repository=route_repository,
            transit_repository=transit_repository,
            route_id=route_id,
            stop_id=stop_id,
        )
    stops = None
    if route_id:
        stops = await get_route_stops_usecase(
            route_repository=route_repository, route_id=route_id
        )
    return await render(
        "browse_lines.html", status=200, context={"user_data": user_data, "routes": routes}
    )


@html_blueprint.get("/login")
async def login(request: Request) -> HTTPResponse:
    return await render("login.html", status=200)


@html_blueprint.get("/signup")
async def signup(request: Request) -> HTTPResponse:
    return await render("signup.html", status=200)


@html_blueprint.get("/stop_crud")
async def stop_crud(request: Request) -> HTTPResponse:
    return await render("manage_stops.html", status=200)


@html_blueprint.get("/edit-line/<line_id>")
async def line_editor(request: Request, line_id: str) -> HTTPResponse:
    return await render("edit_bus_line.html", status=200)


bus_lines_data = [
    {
        'id': 1,
        'name': 'Bus Line 1',
        'stop_count': 10,
        'transits_count': 5
    },
    {
        'id': 2,
        'name': 'Bus Line 2',
        'stop_count': 8,
        'transits_count': 3
    },
    {
        'id': 3,
        'name': 'Bus Line 3',
        'stop_count': 12,
        'transits_count': 7
    }
]


@html_blueprint.route('/bus-lines')
async def bus_lines(request):
    return await render("show_bus_lines.html", status=200, context={"bus_lines": bus_lines_data})
