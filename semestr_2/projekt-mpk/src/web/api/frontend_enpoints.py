from __future__ import annotations

import json
from datetime import time, timedelta, datetime
from random import random

from sanic import Blueprint, HTTPResponse, Request, response
from sanic.log import logger
from sanic.response import json as json_response
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


@html_blueprint.get("/edit-line/<line_id>")
async def line_editor(request: Request, line_id: str) -> HTTPResponse:
    return await render("edit_bus_line.html", status=200)


bus_lines_data = [
    {
        'id': 1,
        'name': 'Bus Line 1',
        'stop_count': 10,
        'transits_count': 5,
        "combined_time": "45 minutes"
    },
    {
        'id': 2,
        'name': 'Bus Line 2',
        'stop_count': 8,
        'transits_count': 3,
        "combined_time": "30 minutes"
    },
    {
        'id': 3,
        'name': 'Bus Line 3',
        'stop_count': 12,
        'transits_count': 7,
        "combined_time": "1h 25 minutes"
    }
]


@html_blueprint.route('/bus-lines')
async def bus_lines(request):
    return await render("show_bus_lines.html", status=200, context={"bus_lines": bus_lines_data})


bus_stops_data = [
    {
        "id": 1,
        "name": "Bus Stop 1",
        "location_x": 10,
        "location_y": 20,
        "bus_line_count": 5,
        "other_stop_connections_count": 3
    },
    {
        "id": 2,
        "name": "Bus Stop 2",
        "location_x": 30,
        "location_y": 40,
        "bus_line_count": 2,
        "other_stop_connections_count": 2
    }
]


@html_blueprint.route('/bus-stops')
async def bus_stops(request):
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


@html_blueprint.route("/api/bus-stops/<stop_id>", methods=["DELETE"])
async def delete_bus_stop(request, stop_id):
    global bus_stops_data
    bus_stops_data = [stop for stop in bus_stops_data if stop["id"] != int(stop_id)]
    return json_response({"message": "Bus stop deleted successfully"})


# Distance data route
@html_blueprint.route("/api/bus-stops/<stop_id>/distances")
async def get_distance_data(request, stop_id):
    # Example distance data for a stop
    distance_data = [
        {"stop_id": 2, "stop_name": "Stop 2", "time": 10},
        {"stop_id": 3, "stop_name": "Stop 3", "time": 15},
        {"stop_id": 4, "stop_name": "Stop 4", "time": 20},
        {"stop_id": 5, "stop_name": "Stop 5", "time": 15},
        {"stop_id": 6, "stop_name": "Stop 6", "time": 40},
    ]

    return json_response({"distances": distance_data})


# Endpoint to search for stops by name
@html_blueprint.route("/api/bus-stops/search", methods=["GET"])
async def search_stops(request):
    search_text = request.args.get("query")

    # Search for stops by name in your data source
    # Example: stops = search_stops_by_name(search_text)

    # Return the search results as JSON response
    stops = [
        {"id": 1,
         "name": "Stop A",
         "location_x": int(random() * 50), "location_y": int(random() * 50),
         "bus_line_count": int(random() * 20), "other_stop_connections_count": int(random() * 20)},
        {"id": 2, "name": "Stop B", "location_x": int(random() * 50), "location_y": int(random() * 50),
         "bus_line_count": int(random() * 20), "other_stop_connections_count": int(random() * 20)},
        {"id": 3, "name": "Stop C", "location_x": int(random() * 50), "location_y": int(random() * 50),
         "bus_line_count": int(random() * 20), "other_stop_connections_count": int(random() * 20)}
    ]
    return json_response({"stops": stops})


@html_blueprint.route("/api/bus-stops/<stop_id>/distances/<other_stop_id>", methods=["PUT"])
async def save_distance_data(request, stop_id, other_stop_id):
    time = request.json.get("time")
    # Save the distance data to the database or perform necessary operations

    return json_response({"message": "Distance data saved successfully"})


# Delete distance data route
@html_blueprint.route("/api/bus-stops/<stop_id>/distances/<other_stop_id>", methods=["DELETE"])
async def delete_distance_data(request, stop_id, other_stop_id):
    # Delete the distance data from the database or perform necessary operations

    return json_response({"message": "Distance data deleted successfully"})


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

transit_data = [
    {
        "id": 1,
        "start_time": " 09:00",
        "end_time": " 09:30",
    },
    {
        "id": 2,
        "start_time": "10:00",
        "end_time": "10:30",
    },
    {
        "id": 3,
        "start_time": " 11:00",
        "end_time": " 11:30",
    },
]


@html_blueprint.route('/edit-line-transits/<line_id>')
async def line_transits(request, line_id: str):
    selected_stop = request.args.get("selected_line")
    selected_stop_id = int(selected_stop) if selected_stop else None

    logger.info(f"selected_stop {selected_stop_id}")
    logger.info(f"transit_lines_data {transit_lines_data}")
    transit_line_data = transit_lines_data[int(line_id)]
    transit_line_data["transits"] = transit_data
    return await render("line_transits.html", status=200,
                        context={"line": transit_line_data})


@html_blueprint.post("/api/transit-add")
async def add_transit(request):
    data = request.json
    line_id = data.get("line_id")
    start_time = time.fromisoformat(data.get("start_time"))

    # Generate a unique ID for the new transit
    new_transit_id = max(transit["id"] for transit in transit_data) + 1

    # Create a new transit object
    new_transit = {
        "id": new_transit_id,
        "start_time": start_time.strftime("%H:%M"),
        "end_time": (datetime.combine(datetime.today(), start_time) + timedelta(minutes=50)).time().strftime("%H:%M")
    }

    # Add the new transit to the list
    transit_data.append(new_transit)

    # Return the new transit as the API response
    return response.json(new_transit)


@html_blueprint.route("/api/lines-search")
async def lines_search(request):
    search_query = request.args.get("search", "")
    search_results = filter_lines(search_query)
    return json_response(search_results)


def filter_lines(search_query):
    # Filter the lines based on the search query
    filtered_lines = [line for line in bus_lines_data if search_query.lower() not in line["name"].lower()]
    return filtered_lines
