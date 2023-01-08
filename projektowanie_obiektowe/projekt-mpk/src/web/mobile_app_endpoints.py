from sanic import Blueprint, json
from sanic.log import logger

from src.web import route_repository, transit_repository, stop_repository
from src.web.mobile_app_usecase import get_all_routes_usecase, get_route_stops_usecase, get_stop_timetable_usecase

mobile_app_blueprint = Blueprint(name="webapp", url_prefix="app")


@mobile_app_blueprint.get("/routes")
async def get_routes(request):
    routes = get_all_routes_usecase(route_repository)
    logger.info(f"routes: {routes}")
    return json(routes)


@mobile_app_blueprint.get("/<route_id>/stops")
async def get_route_stops(request, route_id):
    stops = get_route_stops_usecase(route_repository=route_repository, stops_repository=stop_repository,
                                    route_id=route_id)
    logger.info(f"stops: {stops}")
    return json(stops)


@mobile_app_blueprint.get("/<route_id>/<stop_id>/timetable")
async def get_route_stop_timetable(request, route_id, stop_id):
    time_table = get_stop_timetable_usecase(route_repository=route_repository,
                                            stops_repository=stop_repository,
                                            transit_repository=transit_repository,
                                            route_id=route_id,
                                            stop_id=stop_id
                                            )
    logger.info(f"time_table: {time_table}")
    return json([str(time) for time in time_table])
