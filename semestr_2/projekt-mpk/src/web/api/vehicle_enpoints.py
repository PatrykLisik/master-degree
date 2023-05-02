from dataclasses import asdict

from sanic import Blueprint, HTTPResponse, json, Request
from sanic.log import logger

from src.repositories.abstract import AbstractVehicleRepository
from src.web.api.vehicle_usecase import (
    add_vehicle_usecase,
    get_all_vehicles_usecase,
    get_vehicle_usecase,
    update_vehicle_use_case
)

vehicle_blueprint = Blueprint(name="vehicle")


@vehicle_blueprint.post("/vehicle")
async def add_vehicle(request: Request, vehicle_repository: AbstractVehicleRepository) -> HTTPResponse:
    request_data = request.json
    vehicle = await add_vehicle_usecase(vehicle_repository=vehicle_repository,
                                        capacity=request_data.get("capacity", ""),
                                        )
    return json(asdict(vehicle))


@vehicle_blueprint.get("/vehicle/<vehicle_id>")
async def get_vehicle(request: Request, vehicle_id: str,
                      vehicle_repository: AbstractVehicleRepository) -> HTTPResponse:
    vehicle = await get_vehicle_usecase(vehicle_repository, vehicle_id)
    logger.info(f"vehicle id: {vehicle_id}")
    return json(asdict(vehicle))


@vehicle_blueprint.put("/vehicle/<vehicle_id>")
async def update_vehicle(request: Request,
                         vehicle_id: str,
                         vehicle_repository: AbstractVehicleRepository) -> HTTPResponse:
    request_data = request.json
    vehicle = await update_vehicle_use_case(vehicle_repository=vehicle_repository,
                                            capacity=request_data.get("capacity", None),
                                            vehicle_id=vehicle_id
                                            )
    return json(asdict(vehicle))


@vehicle_blueprint.get("/vehicles")
async def get_all_vehicles(request: Request, vehicle_repository: AbstractVehicleRepository) -> HTTPResponse:
    vehicles = await get_all_vehicles_usecase(vehicle_repository)
    logger.info(f"Vehicles {vehicles}")
    return json([asdict(vehicle) for vehicle in vehicles]
                )
