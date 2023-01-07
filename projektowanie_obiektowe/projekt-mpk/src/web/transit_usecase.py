import datetime
from typing import List

from src.model.frontend_model import Transit
from src.repositories.driver_repository import AbstractDriverRepository
from src.repositories.route_repository import AbstractRouteRepository
from src.repositories.stop_repository import AbstractStopRepository
from src.repositories.transit_repository import AbstractTransitRepository
from src.repositories.vehicle_repository import AbstractVehicleRepository


def add_transit_usecase(transit_repository: AbstractTransitRepository,
                        stops_repo: AbstractStopRepository,
                        route_repo: AbstractRouteRepository,
                        driver_repo: AbstractDriverRepository,
                        vehicle_repo: AbstractVehicleRepository,
                        route_id: str,
                        start_time: datetime,
                        vehicle_id: str,
                        driver_id: str) -> Transit:
    transit = transit_repository.add(route_id, start_time, vehicle_id, driver_id)
    return Transit.form_internal(transit, stops_repo=stops_repo,
                                 route_repo=route_repo,
                                 driver_repo=driver_repo,
                                 vehicle_repo=vehicle_repo)


def get_transit_usecase(transit_repository: AbstractTransitRepository,
                        stops_repo: AbstractStopRepository,
                        route_repo: AbstractRouteRepository,
                        driver_repo: AbstractDriverRepository,
                        vehicle_repo: AbstractVehicleRepository,
                        transit_id) -> Transit:
    return Transit.form_internal(transit_repository.get(transit_id), stops_repo=stops_repo,
                                 route_repo=route_repo,
                                 driver_repo=driver_repo,
                                 vehicle_repo=vehicle_repo)


def get_all_transits_usecase(transit_repository: AbstractTransitRepository,
                             stops_repo: AbstractStopRepository,
                             route_repo: AbstractRouteRepository,
                             driver_repo: AbstractDriverRepository,
                             vehicle_repo: AbstractVehicleRepository,
                             ) -> List[Transit]:
    return [Transit.form_internal(transit,
                                  stops_repo=stops_repo,
                                  route_repo=route_repo,
                                  driver_repo=driver_repo,
                                  vehicle_repo=vehicle_repo)
            for transit in transit_repository.get_all()]
