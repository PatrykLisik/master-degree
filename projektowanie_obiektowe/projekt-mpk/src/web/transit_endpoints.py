from dataclasses import asdict

from sanic import json, Blueprint
from sanic.log import logger

from src.web import transit_repository, driver_repository, vehicle_repository, route_repository, stop_repository
from src.web.transit_usecase import add_transit_usecase, get_transit_usecase, get_all_transits_usecase

transit_blueprint = Blueprint(name="transit")


@transit_blueprint.post("/transit")
async def add_transit(request):
    request_data = request.json
    transit = add_transit_usecase(transit_repository=transit_repository,
                                  driver_repo=driver_repository,
                                  vehicle_repo=vehicle_repository,
                                  route_repo=route_repository,
                                  stops_repo=stop_repository,
                                  vehicle_id=request_data.get("vehicle_id", ""),
                                  driver_id=request_data.get("driver_id", ""),
                                  start_time=request_data.get("start_time"),
                                  route_id=request_data.get("route_id")
                                  )
    return json(asdict(transit))


@transit_blueprint.get("/transit/<transit_id>")
async def get_transit(request, transit_id):
    transit = get_transit_usecase(transit_repository=transit_repository,
                                  driver_repo=driver_repository,
                                  vehicle_repo=vehicle_repository,
                                  route_repo=route_repository,
                                  stops_repo=stop_repository,
                                  transit_id=transit_id)
    logger.info(f"transit id: {transit_id}")
    return json(asdict(transit))


@transit_blueprint.get("/transits")
async def get_all_transits(request):
    transits = get_all_transits_usecase(transit_repository=transit_repository,
                                        driver_repo=driver_repository,
                                        vehicle_repo=vehicle_repository,
                                        route_repo=route_repository,
                                        stops_repo=stop_repository)
    logger.info(f"Transits {transits}")
    return json([asdict(transit) for transit in transits]
                )
