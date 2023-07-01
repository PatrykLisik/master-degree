from __future__ import annotations

from datetime import time, datetime, timedelta
from random import randint

from pydantic import BaseModel, Field
from sanic import Blueprint, json as json_response, response
from sanic_ext import validate
from sanic_ext.extensions.openapi import openapi


api_blueprint = Blueprint(name="api", url_prefix="/")
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


@api_blueprint.delete("/api/bus-stops/<stop_id>")
async def delete_bus_stop(request, stop_id):
    global bus_stops_data
    bus_stops_data = [stop for stop in bus_stops_data if stop["id"] != int(stop_id)]
    return json_response({"message": "Bus stop deleted successfully"})


@api_blueprint.route("/api/bus-stops/<stop_id>/distances")
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


@api_blueprint.route("/api/bus-stops/<stop_id>/distances/<other_stop_id>", methods=["PUT"])
async def save_distance_data(request, stop_id, other_stop_id):
    time = request.json.get("time")
    # Save the distance data to the database or perform necessary operations

    return json_response({"message": "Distance data saved successfully"})


@api_blueprint.route("/api/bus-stops/<stop_id>/distances/<other_stop_id>", methods=["DELETE"])
async def delete_distance_data(request, stop_id, other_stop_id):
    # Delete the distance data from the database or perform necessary operations

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
async def add_transit(request, body):

    # Generate a unique ID for the new transit
    new_transit_id = max(transit["id"] for transit in transit_data) + 1

    # Create a new transit object
    new_transit = {
        "id": new_transit_id,
        "start_time": body.start_time.strftime("%H:%M"),
        "end_time": (datetime.combine(datetime.today(), body.start_time) + timedelta(minutes=50)).time().strftime("%H:%M")
    }

    # Add the new transit to the list
    transit_data.append(new_transit)

    # Return the new transit as the API response
    return response.json(new_transit)


@api_blueprint.route("/api/lines-search")
async def lines_search(request):
    search_query = request.args.get("search", "")
    search_results = filter_lines(search_query)
    return json_response(search_results)


def filter_lines(search_query):
    # Filter the lines based on the search query
    filtered_lines = [line for line in bus_lines_data if search_query.lower() not in line["name"].lower()]
    return filtered_lines


class BusStop(BaseModel):
    stop_name: str = Field(description="Name of the stop")
    x_position: int = Field(description="X position of the stop")
    y_position: int = Field(description="Y position of the stop")


@api_blueprint.post("/api/add_stop")
@openapi.definition(
    body={"application/json": BusStop.model_json_schema()},
)
@validate(json=BusStop)
async def add_stop(request, body:BusStop):
    print(body)
    return json_response({"message": "Stop added successfully"})


@api_blueprint.route("/api/bus-stops/search", methods=["GET"])
@openapi.summary("Search bus stops by name")
@openapi.parameter("query", str, description="Search query", required=True, example="Bus Stop")
async def search_stops(request):
    search_text = request.args.get("query")

    # Search for stops by name in your data source
    # Example: stops = search_stops_by_name(search_text)

    # Generate random stop data
    stops = {}
    for i in range(randint(1, 1000)):
        stop = {
            "id": i,
            "name": f"Stop {chr(65 + i)}",
            "location_x": randint(0, 50),
            "location_y": randint(0, 50),
            "bus_line_count": randint(0, 20),
            "other_stop_connections_count": randint(0, 20)
        }
        stops[i]=stop

    return json_response({"stops": stops})
