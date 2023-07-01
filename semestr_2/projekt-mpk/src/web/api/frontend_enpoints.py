from __future__ import annotations

import json

from sanic import Blueprint, Request
from sanic.log import logger
from sanic_ext import render
from sanic_ext.extensions.templating.render import TemplateResponse

from src.repositories.abstract import AbstractRouteRepository, AbstractTransitRepository
from src.web.api import COOKIE_KEY
from src.web.api.api import transit_data, bus_lines_data, bus_stops_data
from src.web.api.mobile_app_usecase import get_all_routes_usecase, get_route_stops_usecase, get_stop_timetable_usecase

html_blueprint = Blueprint(name="frontend", url_prefix="/")


@html_blueprint.get("/")
async def index(request: Request,
                route_repository: AbstractRouteRepository,
                ) -> TemplateResponse:
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
                           ) -> TemplateResponse:
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
                                             ) -> TemplateResponse:
    if not route_id or not stop_id:
        return TemplateResponse(status=418)
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
async def login(request: Request) -> TemplateResponse:
    return await render("login.html", status=200)


@html_blueprint.get("/signup")
async def signup(request: Request) -> TemplateResponse:
    return await render("signup.html", status=200)


@html_blueprint.get("/edit-line/<line_id>")
async def line_editor(request: Request, line_id: str) -> TemplateResponse:
    return await render("edit_bus_line.html", status=200)


transit_lines_data: dict[int, dict] = {
    1: {
        "id": 1,
        "name": "Line 1",
        "transits_count": 10,
        "stop_count": 5,
        "combined_time": "1 hour"
    },
    2: {
        "id": 2,
        "name": "Line 2",
        "transits_count": 8,
        "stop_count": 7,
        "combined_time": "45 minutes"
    },
    3: {
        "id": 3,
        "name": "Line 3",
        "transits_count": 12,
        "stop_count": 4,
        "combined_time": "1 hour 30 minutes"
    }
}


@html_blueprint.route('/edit-line-transits/<line_id>')
async def line_transits(request, line_id: str) -> TemplateResponse:
    selected_stop = request.args.get("selected_line")
    selected_stop_id = int(selected_stop) if selected_stop else None

    logger.info(f"selected_stop {selected_stop_id}")
    logger.info(f"transit_lines_data {transit_lines_data}")
    transit_line_data = transit_lines_data[int(line_id)]
    transit_line_data["transits"] = transit_data
    return await render("line_transits.html", status=200,
                        context={"line": transit_line_data})


@html_blueprint.route('/bus-lines')
async def bus_lines(request) -> TemplateResponse:
    return await render("show_bus_lines.html", status=200, context={"bus_lines": bus_lines_data})


@html_blueprint.route('/bus-stops')
async def bus_stops(request) -> TemplateResponse:
    selected_stop = request.args.get("selected_stop")
    selected_stop_id = int(selected_stop) if selected_stop else None

    distance_data = None
    if selected_stop_id:
        distance_data = [
            {"stop_id": 2, "stop_name": "Stop 2", "time": 10},
            {"stop_id": 3, "stop_name": "Stop 3", "time": 15},
        ]

    logger.info(f"selected_stop {selected_stop_id}")
    return await render("show_bus_line_stops.html", status=200,
                        context={"bus_stops": bus_stops_data, "selected_stop_id": selected_stop_id,
                                 "distances": distance_data})
