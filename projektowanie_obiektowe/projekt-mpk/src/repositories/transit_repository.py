import json
import uuid
from abc import ABC, abstractmethod
from dataclasses import asdict
from datetime import datetime
from typing import Set, Dict, Optional

from sanic.log import logger

from src.model.internal_model import Transit


class AbstractTransitRepository(ABC):

    @abstractmethod
    def add(self,
            route_id: str,
            start_time: datetime,
            vehicle_id: str,
            driver_id: str) -> Transit:
        raise NotImplementedError

    @abstractmethod
    def update(self, transit_id: str, updated_transit: Transit):
        raise NotImplementedError

    @abstractmethod
    def get(self, transit_id: str) -> Transit:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> Set[Transit]:
        raise NotImplementedError


class InFileTransitRepository(AbstractTransitRepository):
    _file_name = "data/transits.json"

    def _get(self) -> Dict[str, Transit]:
        try:
            with open(self._file_name, "r+", ) as infile:
                logger.info("load stops")
                data = json.load(infile)
                return {transit_data["id"]: Transit(
                    id=transit_data["id"],
                    route_id=transit_data["route_id"],
                    vehicle_id=transit_data["vehicle_id"],
                    driver_id=transit_data["driver_id"],
                    start_time=datetime.fromisoformat(transit_data["start_time"])
                )
                    for transit_data in data}
        except FileNotFoundError:
            logger.info("load stop file doest not exist")
            return {}

    def _set(self, transits: Dict[str, Transit]):
        logger.info("save transits")
        transits_to_save = [asdict(transit) for transit in transits.values()]
        json_to_save = json.dumps(transits_to_save, indent=4, default=str)
        with open(self._file_name, "w+") as outfile:
            outfile.write(json_to_save)

    def add(self,
            route_id: str,
            start_time: datetime,
            vehicle_id: str,
            driver_id: str) -> Transit:
        new_transit = Transit(route_id=route_id, start_time=start_time, vehicle_id=vehicle_id, driver_id=driver_id,
                              id=str(uuid.uuid4()))
        transits = self._get()
        transits[new_transit.id] = new_transit
        self._set(transits)
        return new_transit

    def update(self, transit_id: str, updated_transit: Transit):
        transits = self._get()
        transits[updated_transit.id] = updated_transit
        self._set(transits)

    def get(self, transit_id: str) -> Optional[Transit]:
        transits = self._get()
        return transits.get(transit_id, None)

    def get_all(self) -> Set[Transit]:
        return set(self._get().values())
