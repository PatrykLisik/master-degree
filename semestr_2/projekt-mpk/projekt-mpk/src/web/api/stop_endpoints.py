from dataclasses import asdict

from sanic import json, Blueprint
from sanic.log import logger

from src.web import stop_repository
from src.web.api.stop_usecase import add_stop_usecase, get_stop_usecase, get_all_stop_usecase, \
    add_time_between_stops_usecase

stop_blueprint = Blueprint(name="stops")


@stop_blueprint.post("/stop")
async def add_stop(request):
    request_data = request.json
    stop = await add_stop_usecase(
        stop_repository=stop_repository,
        name=request_data.get("name"),
        geo_x=request_data.get("loc_x", ""),
        geo_y=request_data.get("loc_y", " ")
    )
    return json(asdict(stop))


@stop_blueprint.post("/stop/set_time_to_stop")
async def add_time_between_stops(request):
    request_data = request.json
    await add_time_between_stops_usecase(
        stop_repository=stop_repository,
        start_stop_id=request_data.get("start_stop_id"),
        end_stop_id=request_data.get("end_stop_id"),
        time_in_sec=request_data.get("time_in_s")
    )
    return json({})


@stop_blueprint.get("/stop/<stop_id>")
async def get_stop(request, stop_id):
    stop = await get_stop_usecase(stop_repository, stop_id)
    logger.info(f"stop: {stop}")
    return json(asdict(stop))


@stop_blueprint.get("/stops")
async def get_all_stops(request):
    stops = await get_all_stop_usecase(stop_repository)
    return json([asdict(stop) for stop in stops])
