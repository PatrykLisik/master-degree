from sanic import json, Blueprint
from sanic.log import logger

from src.repositories.driver_repository import InMemoryDriverRepository
from src.web.driver_usecase import add_driver_usecase, get_driver_usecase, get_all_drivers_usecase, \
    update_driver_use_case

driver_repository = InMemoryDriverRepository()

backoffice_blueprint = Blueprint(name="backoffice", url_prefix="backoffice/")


@backoffice_blueprint.post("/driver")
async def add_driver(request):
    request_data = request.json
    driver = add_driver_usecase(driver_repository=driver_repository, name=request_data.get("name", ""),
                                pesel=request_data.get("pesel", ""),
                                phone=request_data.get("phone", ""),
                                surname=request_data.get("surname", ""))
    return json({
        "name": driver.first_name,
        "surname": driver.last_name,
        "phone": driver.phone,
        "pesel": driver.PESEL,
        "id": driver.id
    })


@backoffice_blueprint.get("/driver/<driver_id>")
async def get_driver(request, driver_id):
    driver = get_driver_usecase(driver_repository, driver_id)
    logger.info(f"driver id: {driver_id}")
    return json({
        "name": driver.first_name,
        "surname": driver.last_name,
        "phone": driver.phone,
        "pesel": driver.PESEL,
        "id": driver.id
    })


@backoffice_blueprint.put("/driver/<driver_id>")
async def update_driver(request, driver_id):
    request_data = request.json
    driver = update_driver_use_case(driver_repository=driver_repository, name=request_data.get("name", None),
                                    pesel=request_data.get("pesel", None),
                                    phone=request_data.get("phone", None),
                                    surname=request_data.get("surname", None),
                                    driver_id=driver_id
                                    )
    return json({
        "name": driver.first_name,
        "surname": driver.last_name,
        "phone": driver.phone,
        "pesel": driver.PESEL,
        "id": driver.id
    })


@backoffice_blueprint.get("/drivers")
async def get_all_drivers(request):
    drivers = get_all_drivers_usecase(driver_repository)
    logger.info(f"Drivers {drivers}")
    return json([{
        "name": driver.first_name,
        "surname": driver.last_name,
        "phone": driver.phone,
        "pesel": driver.PESEL,
        "id": driver.id
    } for driver in drivers]
    )
