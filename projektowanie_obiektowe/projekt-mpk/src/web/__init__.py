from src.repositories.driver_repository import InFileDriverRepository
from src.repositories.route_repository import InFileRouteRepository
from src.repositories.stop_repository import FileStopRepository

driver_repository = InFileDriverRepository()
stop_repository = FileStopRepository()
route_repository = InFileRouteRepository(stop_repo=stop_repository)
