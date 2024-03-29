from __future__ import annotations

from datetime import time, timedelta

from pydantic import BaseModel, Field
from sanic import Blueprint, json as json_response, response
from sanic.response import JSONResponse
from sanic_ext import validate
from sanic_ext.extensions.openapi import openapi

from src.repositories.abstract import (
    AbstractStopRepository,
    AbstractRouteRepository,
    AbstractTransitRepository,
)

api_blueprint = Blueprint(name="api", url_prefix="/")


@api_blueprint.delete("/api/bus-stops/<stop_id>")
async def delete_bus_stop(
        request, stop_repo: AbstractStopRepository, stop_id
) -> JSONResponse:
    await stop_repo.delete(stop_id)
    return json_response({"message": "Bus stop deleted successfully"})


@api_blueprint.delete("/api/bus-line/<stop_id>")
async def delete_bus_line(
        request, route_repo: AbstractRouteRepository, stop_id
) -> JSONResponse:
    await route_repo.delete(stop_id)
    return json_response({"message": "Bus stop deleted successfully"})


@api_blueprint.delete("/api/transit/<transit_id>")
async def delete_transit(
        request, transit_repo: AbstractTransitRepository, transit_id
) -> JSONResponse:
    await transit_repo.delete(transit_id)
    return json_response({"message": "Transit deleted successfully"})


@api_blueprint.route("/api/bus-stops/<stop_id>/distances")
async def get_distance_data(
        request, stop_repo: AbstractStopRepository, stop_id: str
) -> JSONResponse:
    stop = await stop_repo.get(stop_id)

    # Example distance data for a stop
    distance_data = [
        {
            "stop_id": stop.id,
            "stop_name": stop.name,
            "time": time_to_given_stop.minues(),
        }
        for stop, time_to_given_stop in stop.time_to_other_stops
    ]

    return json_response({"distances": distance_data})


class TimeBetweenStops(BaseModel):
    stop_id: str = Field(description="ID of the stop")
    other_stop_id: str = Field(description="ID of target stop")
    time: int = Field(description="travel time in mins")


@api_blueprint.route("/api/set-times-between-stops", methods=["POST", "PUT"])
@openapi.definition(
    body={"application/json": TimeBetweenStops.model_json_schema()},
)
@validate(json=TimeBetweenStops)
async def save_distance_data(
        request, stop_repo: AbstractStopRepository, body: TimeBetweenStops
) -> JSONResponse:
    await stop_repo.set_time_between_stops(
        body.stop_id, body.other_stop_id, timedelta(minutes=body.time)
    )
    return json_response({"message": "Distance data saved successfully"})


@api_blueprint.delete("/api/bus-stops/<stop_id>/distance/<other_stop_id>")
async def delete_distance_data(
        request, stop_repo: AbstractStopRepository, stop_id, other_stop_id
) -> JSONResponse:
    # Delete the distance data from the database or perform necessary operations
    await stop_repo.delete_time_between_stops(stop_id, other_stop_id)
    return json_response({"message": "Distance data deleted successfully"})


class TransitData(BaseModel):
    line_id: int = Field(description="ID of the transit line")
    start_time: time = Field(description="Start time of the transit in ISO format")


@api_blueprint.post("/api/transit-add")
@openapi.definition(
    body={"application/json": TransitData.model_json_schema()},
)
@validate(json=TransitData)
async def add_transit(
        request, transit_repo: AbstractTransitRepository, body: TransitData
) -> JSONResponse:
    await transit_repo.add(route_id=str(body.line_id), start_time=body.start_time)

    return response.json({"message": "Transit added"})


@api_blueprint.route("/api/lines-search")
async def lines_search(request, route_repo: AbstractRouteRepository) -> JSONResponse:
    search_query: str = request.args.get("search", "")
    # if search_query:
    #     search_query = search_query.lower()
    search_results = await route_repo.search_by_name(f"%{search_query}%")
    bus_lines_data = [
        {
            "id": route.id,
            "name": route.name,
            "stop_count": len(route.stops),
            "transits_count": len(route.transits),
            "combined_time": str(route.combined_time),
        }
        for route in search_results
    ]
    return json_response(bus_lines_data)


class AddBusLine(BaseModel):
    name: str = Field(description="Name of the line")


@api_blueprint.post("/api/line-add")
@openapi.definition(
    body={"application/json": AddBusLine.model_json_schema()},
)
@validate(json=AddBusLine)
async def add_route(
        request, route_repo: AbstractRouteRepository, body: AddBusLine
) -> JSONResponse:
    await route_repo.add(body.name)
    return json_response({"message": "Route added successfully"})


class BusStop(BaseModel):
    stop_name: str = Field(description="Name of the stop")
    x_position: float = Field(description="X position of the stop")
    y_position: float = Field(description="Y position of the stop")


@api_blueprint.post("/api/add_stop")
@openapi.definition(
    body={"application/json": BusStop.model_json_schema()},
)
@validate(json=BusStop)
async def add_stop(
        request, stop_repo: AbstractStopRepository, body: BusStop
) -> JSONResponse:
    await stop_repo.add(
        body.stop_name, geolocation_x=body.x_position, geolocation_y=body.y_position
    )
    return json_response({"message": "Stop added successfully"})


@api_blueprint.get("/api/bus-stops/search")
@openapi.summary("Search bus stops by name")
@openapi.parameter(
    "query", str, description="Search query", required=True, example="Bus Stop"
)
async def search_stops(request, stop_repo: AbstractStopRepository) -> JSONResponse:
    search_text = request.args.get("query")
    stops = []
    if search_text is not None:
        search_text = search_text.strip().replace(" ", "%")
        search_text = f"%{search_text}%"
        for domain_stop in await stop_repo.search_by_name(search_text):
            stop = {
                "id": domain_stop.id,
                "name": domain_stop.name,
                "location_x": domain_stop.loc_x,
                "location_y": domain_stop.loc_x,
                "bus_line_count": 0,
                "other_stop_connections_count": len(domain_stop.time_to_other_stops),
            }
            stops.append(stop)

    return json_response({"stops": stops})
