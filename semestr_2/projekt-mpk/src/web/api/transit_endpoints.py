from dataclasses import asdict

from sanic import Blueprint, HTTPResponse, json
from sanic.log import logger

from src.repositories.abstract import AbstractTransitRepository
from src.web.api.transit_usecase import add_transit_usecase, get_all_transits_usecase, get_transit_usecase

transit_blueprint = Blueprint(name="transit")


@transit_blueprint.post("/transit")
async def add_transit(request, transit_repository: AbstractTransitRepository) -> HTTPResponse:
    request_data = request.json
    transit = await add_transit_usecase(transit_repository=transit_repository,
                                  vehicle_id=request_data.get("vehicle_id", ""),
                                  driver_id=request_data.get("driver_id", ""),
                                  start_time=request_data.get("start_time"),
                                  route_id=request_data.get("route_id")
                                  )
    return json(asdict(transit))


@transit_blueprint.get("/transit/<transit_id>")
async def get_transit(request, transit_id, transit_repository: AbstractTransitRepository) -> HTTPResponse:
    transit = await get_transit_usecase(transit_repository=transit_repository,
                                  transit_id=transit_id)
    logger.info(f"transit id: {transit_id}")
    return json(asdict(transit))


@transit_blueprint.get("/transits")
async def get_all_transits(request, transit_repository: AbstractTransitRepository) -> HTTPResponse:
    transits = await get_all_transits_usecase(transit_repository=transit_repository)
    logger.info(f"Transits {transits}")
    return json([asdict(transit) for transit in transits])
