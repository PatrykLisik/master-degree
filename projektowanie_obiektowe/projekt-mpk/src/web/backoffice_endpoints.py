from dataclasses import asdict

from sanic import json, Blueprint

from src.repositories.driver_repository import FakeDriverRepository
from src.web.backoffice_usecase import add_driver_usecase

backoffice_blueprint = Blueprint(name="backoffice", url_prefix="backoffice/")

driver_repository = FakeDriverRepository()


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
        "pesel": driver.PESEL
    })
