from __future__ import annotations

from datetime import time, datetime, timedelta

from pydantic import BaseModel, Field
from sanic import Blueprint, json as json_response, response
from sanic.response import JSONResponse
from sanic_ext import validate
from sanic_ext.extensions.openapi import openapi

from src.repositories.abstract import AbstractStopRepository

api_blueprint = Blueprint(name="api", url_prefix="/")
bus_lines_data = [
    {
        "id": 1,
        "name": "Bus Line 1",
        "stop_count": 10,
        "transits_count": 5,
        "combined_time": "45 minutes",
    },
    {
        "id": 2,
        "name": "Bus Line 2",
        "stop_count": 8,
        "transits_count": 3,
        "combined_time": "30 minutes",
    },
    {
        "id": 3,
        "name": "Bus Line 3",
        "stop_count": 12,
        "transits_count": 7,
        "combined_time": "1h 25 minutes",
    },
]


@api_blueprint.delete("/api/bus-stops/<stop_id>")
async def delete_bus_stop(
    request, stop_repo: AbstractStopRepository, stop_id
) -> JSONResponse:
    await stop_repo.delete(stop_id)
    return json_response({"message": "Bus stop deleted successfully"})


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
async def delete_distance_data(request,stop_repo: AbstractStopRepository, stop_id, other_stop_id) -> JSONResponse:
    # Delete the distance data from the database or perform necessary operations
    await stop_repo.delete_time_between_stops(stop_id, other_stop_id)
    return json_response({"message": "Distance data deleted successfully"})


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


class TransitData(BaseModel):
    line_id: int = Field(description="ID of the transit line")
    start_time: time = Field(description="Start time of the transit in ISO format")


@api_blueprint.post("/api/transit-add")
@openapi.definition(
    body={"application/json": TransitData.model_json_schema()},
)
@validate(json=TransitData)
async def add_transit(request, body) -> JSONResponse:
    # Generate a unique ID for the new transit
    new_transit_id = max(transit["id"] for transit in transit_data) + 1

    # Create a new transit object
    new_transit = {
        "id": new_transit_id,
        "start_time": body.start_time.strftime("%H:%M"),
        "end_time": (
            datetime.combine(datetime.today(), body.start_time) + timedelta(minutes=50)
        )
        .time()
        .strftime("%H:%M"),
    }

    # Add the new transit to the list
    transit_data.append(new_transit)

    # Return the new transit as the API response
    return response.json(new_transit)


@api_blueprint.route("/api/lines-search")
async def lines_search(request) -> JSONResponse:
    search_query = request.args.get("search", "")
    search_results = filter_lines(search_query)
    return json_response(search_results)


def filter_lines(search_query):
    # Filter the lines based on the search query
    filtered_lines = [
        line
        for line in bus_lines_data
        if search_query.lower() not in line["name"].lower()
    ]
    return filtered_lines


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
