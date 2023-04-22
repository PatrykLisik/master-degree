from src.repositories.driver_repository import InFileDriverRepository
from src.repositories.route_repository import InFileRouteRepository
from src.repositories.stop_repository import FileStopRepository
from src.repositories.transit_repository import InFileTransitRepository
from src.repositories.vehicle_repository import InFileVehicleRepository

driver_repository = InFileDriverRepository()
stop_repository = FileStopRepository()
route_repository = InFileRouteRepository()
vehicle_repository = InFileVehicleRepository()
transit_repository = InFileTransitRepository()
