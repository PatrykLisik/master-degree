from sanic import json, Blueprint

from src.repositories.stop_repository import FileStopRepository
from src.web.stop_usecase import add_stop_usecase

infile_stop_repository = FileStopRepository()

stop_blueprint = Blueprint(name="stops")


@stop_blueprint.post("/stop")
async def add_driver(request):
    request_data = request.json
    stop = await add_stop_usecase(
        stop_repository=infile_stop_repository,
        name=request_data.get("name"),
        geo_x=request_data.get("loc_x", ""),
        geo_y=request_data.get("loc_y", " ")
    )
    return json({
        "name": stop.name,
        "time_to_other_stops": stop.time_to_other_stops,
        "geolocation": stop.geolocation,
        "id": stop.id
    })
