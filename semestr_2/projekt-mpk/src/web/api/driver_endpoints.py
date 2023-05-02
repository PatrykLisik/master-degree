from dataclasses import asdict

from sanic import Blueprint, HTTPResponse, json
from sanic.log import logger

from src.repositories.abstract import AbstractDriverRepository
from src.web.api.driver_usecase import (
    add_driver_usecase,
    get_all_drivers_usecase,
    get_driver_usecase,
    update_driver_use_case,
)

driver_blueprint = Blueprint(name="driver", url_prefix="backoffice/")


@driver_blueprint.post("/driver")
async def add_driver(
    request, driver_repository: AbstractDriverRepository
) -> HTTPResponse:
    request_data = request.json
    driver = await add_driver_usecase(
        driver_repository=driver_repository,
        name=request_data.get("name", ""),
        pesel=request_data.get("pesel", ""),
        phone=request_data.get("phone", ""),
        surname=request_data.get("surname", ""),
    )
    return json(asdict(driver))


@driver_blueprint.get("/driver/<driver_id>")
async def get_driver(
    request, driver_id, driver_repository: AbstractDriverRepository
) -> HTTPResponse:
    driver = await get_driver_usecase(driver_repository, driver_id)
    logger.info(f"driver id: {driver_id}")
    return json(asdict(driver))


@driver_blueprint.put("/driver/<driver_id>")
async def update_driver(
    request, driver_id, driver_repository: AbstractDriverRepository
) -> HTTPResponse:
    request_data = request.json
    driver = await update_driver_use_case(
        driver_repository=driver_repository,
        name=request_data.get("name", None),
        pesel=request_data.get("pesel", None),
        phone=request_data.get("phone", None),
        surname=request_data.get("surname", None),
        driver_id=driver_id,
    )
    return json(asdict(driver))


@driver_blueprint.get("/drivers")
async def get_all_drivers(
    request, driver_repository: AbstractDriverRepository
) -> HTTPResponse:
    drivers = await get_all_drivers_usecase(driver_repository)
    logger.info(f"Drivers {drivers}")
    return json([asdict(driver) for driver in drivers])
