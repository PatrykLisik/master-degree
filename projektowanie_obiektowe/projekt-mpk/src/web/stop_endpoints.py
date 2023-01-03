from sanic import json, Blueprint
from sanic.log import logger

from src.repositories.stop_repository import FileStopRepository
from src.web.stop_usecase import add_stop_usecase, get_stop_usecase, get_all_stop_usecase, \
    add_time_between_stops_usecase

infile_stop_repository = FileStopRepository()

stop_blueprint = Blueprint(name="stops")


@stop_blueprint.post("/stop")
async def add_stop(request):
    request_data = request.json
    stop = await add_stop_usecase(
        stop_repository=infile_stop_repository,
        name=request_data.get("name"),
        geo_x=request_data.get("loc_x", ""),
        geo_y=request_data.get("loc_y", " ")
    )
    return json(stop_to_return_model(stop))


@stop_blueprint.post("/stop/set_time_to_stop")
async def add_time_between_stops(request):
    request_data = request.json
    await add_time_between_stops_usecase(
        stop_repository=infile_stop_repository,
        start_stop_id=request_data.get("start_stop_id"),
        end_stop_id=request_data.get("end_stop_id"),
        time_in_sec=request_data.get("time_in_s")
    )
    return json({})


@stop_blueprint.get("/stop/<stop_id>")
async def get_stop(request, stop_id):
    stop = await get_stop_usecase(infile_stop_repository, stop_id)
    logger.info(f"stop: {stop}")
    return json(stop_to_return_model(stop))


def stop_to_return_model(stop):
    return {
        "name": stop.name,
        "time_to_other_stops": {stop_id: str(time) for stop_id, time in stop.time_to_other_stops.items()},
        "geolocation": stop.geolocation,
        "id": stop.id
    }


@stop_blueprint.get("/stops")
async def get_all_stops(request):
    stops = await get_all_stop_usecase(infile_stop_repository)
    return json([stop_to_return_model(stop) for stop in stops])
