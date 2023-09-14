from __future__ import annotations

import json
from datetime import datetime, date

from sanic import Blueprint, Request
from sanic.log import logger
from sanic_ext import render
from sanic_ext.extensions.templating.render import TemplateResponse

from src.repositories.abstract import (
    AbstractRouteRepository,
    AbstractTransitRepository,
    AbstractStopRepository,
)
from src.web.api import COOKIE_KEY
from src.web.api.mobile_app_usecase import (
    get_all_routes_usecase,
    get_route_stops_usecase,
    get_stop_timetable_usecase,
)

html_blueprint = Blueprint(name="frontend", url_prefix="/")


@html_blueprint.get("/browse-lines/")
async def index(
        request: Request,
        route_repository: AbstractRouteRepository,
) -> TemplateResponse:
    user_data = request.cookies.get(COOKIE_KEY, {})
    if user_data:
        user_data = json.loads(user_data)
    logger.debug(f"Cookie {user_data}")

    routes = await get_all_routes_usecase(route_repository)
    logger.debug(f"Routes: {routes}")
    return await render(
        "browse_lines.html",
        status=200,
        context={"user_data": user_data,
                 "routes": routes,
                 "current_route": None,
                 "transits": []
                 },
    )


@html_blueprint.get("/browse-lines/<route_id>/")
async def index_with_route(
        request: Request,
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
        "browse_lines.html",
        status=200,
        context={
            "user_data": user_data,
            "routes": routes,
            "current_route": route_id,
            "stops": stops,
            "transits": []
        },
    )


@html_blueprint.get("/browse-lines/<route_id>/<stop_id>/")
async def index_with_route_and_stop_selected(
        request: Request,
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

    stops = await get_route_stops_usecase(
        route_repository=route_repository, route_id=route_id
    )

    transits = None
    if route_id and stop_id:
        time_table = await get_stop_timetable_usecase(
            route_repository=route_repository,
            transit_repository=transit_repository,
            route_id=route_id,
            stop_id=stop_id,
        )
        transits = []
        for time in time_table:
            transits.append(f"{time.hour:02d}:{time.minute:02d}")

    return await render(
        "browse_lines.html",
        status=200,
        context={
            "user_data": user_data,
            "routes": routes,
            "current_route": route_id,
            "stops": stops,
            "transits": transits
},
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


@html_blueprint.route("/edit-line-transits/<line_id>")
async def line_transits(
        request, bus_line_repo: AbstractRouteRepository, line_id: str
) -> TemplateResponse:
    if not line_id:
        raise ValueError("Bus line does not exist")
    bus_line = await bus_line_repo.get(line_id)

    transit_line_data = {
        "id": bus_line.id,
        "name": bus_line.name,
        "transits_count": len(bus_line.transits),
        "combined_time": str(bus_line.combined_time),
        "transits": [
            {
                "id": transit.id,
                "start_time": transit.start_time.strftime("%H:%M"),
                "end_time": (
                        datetime.combine(date.today(), transit.start_time)
                        + bus_line.combined_time
                ).strftime("%H:%M"),
            }
            for transit in bus_line.transits
        ],
    }
    return await render(
        "line_transits.html", status=200, context={"line": transit_line_data}
    )


@html_blueprint.route("/bus-lines")
async def bus_lines(
        request, bus_line_repo: AbstractRouteRepository
) -> TemplateResponse:
    routes = await bus_line_repo.get_all()
    bus_lines_data = [
        {
            "id": route.id,
            "name": route.name,
            "stop_count": len(route.stops),
            "transits_count": len(route.transits),
            "combined_time": route.combined_time,
        }
        for route in routes
    ]
    return await render(
        "show_bus_lines.html", status=200, context={"bus_lines": bus_lines_data}
    )


@html_blueprint.route("/bus-stops")
async def bus_stops(request, stop_repo: AbstractStopRepository) -> TemplateResponse:
    selected_stop_id = request.args.get("selected_stop")
    target_stop_id = request.args.get("target_stop")

    bus_stops_domain_data = await stop_repo.get_all()

    bus_stops_data = [
        {
            "id": bus_stop.id,
            "name": bus_stop.name,
            "location_x": bus_stop.loc_x,
            "location_y": bus_stop.loc_x,
            "bus_line_count": 0,
            "other_stop_connections_count": len(bus_stop.time_to_other_stops),
        }
        for bus_stop in bus_stops_domain_data
    ]
    logger.info(f"bus_stops_data {bus_stops_data}")
    distance_data = None
    if selected_stop_id:
        bus_stop = await stop_repo.get(selected_stop_id)
        cs_stop = {
            "id": bus_stop.id,
            "name": bus_stop.name,
            "location_x": bus_stop.loc_x,
            "location_y": bus_stop.loc_x,
            "bus_line_count": 0,
            "other_stop_connections_count": len(bus_stop.time_to_other_stops),
        }
        bus_stops_data = [
            stop for stop in bus_stops_data if int(stop["id"]) != int(selected_stop_id)
        ]
        bus_stops_data.insert(0, cs_stop)

        ids_to_fetch = {int(stop["id"]) for stop in bus_stops_data}
        distance_stops = await stop_repo.get_many(ids_to_fetch)
        id_to_stop = {stop.id: stop for stop in distance_stops}
        distance_data = [
            {
                "stop_id": end_stop_id,
                "stop_name": id_to_stop[int(end_stop_id)].name,
                "time": time.seconds / 60,
            }
            for end_stop_id, time in bus_stop.time_to_other_stops.items()
        ]

    logger.info(f"selected_stop {selected_stop_id}")
    return await render(
        "show_bus_line_stops.html",
        status=200,
        context={
            "bus_stops": bus_stops_data,
            "selected_stop_id": int(selected_stop_id) if selected_stop_id else None,
            "target_stop_id": int(target_stop_id) if target_stop_id else None,
            "distances": distance_data,
        },
    )
