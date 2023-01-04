import decimal
import json
import uuid
from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Set, Dict

from sanic.log import logger

from src.model.internal_model import Stop


class AbstractStopRepository(ABC):

    @abstractmethod
    def add(self, name: str, geolocation_x: decimal, geolocation_y: decimal) -> Stop:
        raise NotImplementedError

    @abstractmethod
    def update(self, stop_id: str, updated_stop: Stop):
        raise NotImplementedError

    @abstractmethod
    def get(self, stop_id: str) -> Stop:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> Set[Stop]:
        raise NotImplementedError

    @abstractmethod
    def get_many(self, stop_ids: set[str]) -> Set[Stop]:
        raise NotImplementedError

    @abstractmethod
    def set_time_between_stops(self, start_stop_id: str, end_stop_id: str, time: timedelta):
        raise NotImplementedError


class InMemoryStopRepository(AbstractStopRepository):
    _stops = {}

    def add(self, name: str, geolocation_x: decimal, geolocation_y: decimal) -> Stop:
        new_stop = Stop(name=name,
                        geolocation=(geolocation_x, geolocation_y),
                        time_to_other_stops={},
                        id=str(uuid.uuid4()))
        self._stops[new_stop.id] = new_stop
        return new_stop

    def update(self, stop_id: str, updated_stop: Stop):
        self._stops[stop_id] = updated_stop

    def get(self, stop_id: str) -> Stop:
        return self._stops[stop_id]

    def get_all(self) -> Set[Stop]:
        return set(self._stops.values())

    def get_many(self, stop_ids: set[str]) -> Set[Stop]:
        return {value for value in self._stops.values() if value.id in stop_ids}

    def set_time_between_stops(self, start_stop_id: str, end_stop_id: str, time: timedelta):
        start_stop = self.get(start_stop_id)
        start_stop.time_to_other_stops[end_stop_id] = time


class FileStopRepository(AbstractStopRepository):
    _file_name = "stop.json"

    def _get_stops(self) -> Dict[str, Stop]:

        try:
            with open(self._file_name, "r+", ) as infile:
                logger.info("load stops")
                data = json.load(infile)
                return {stop_data["id"]: Stop(
                    id=stop_data["id"],
                    name=stop_data["name"],
                    geolocation=(stop_data["x"], stop_data["y"]),
                    time_to_other_stops={times["stop_id"]: timedelta(seconds=times["time_in_sec"])
                                         for times in stop_data["time_to_other_stops"]}
                )
                    for stop_data in data}
        except FileNotFoundError:
            logger.info("load stop file doest not exist")
            return {}

    def _set_stops(self, stops: Dict[str, Stop]):
        logger.info("save stops")
        stops_to_save = [{
            "id": stop.id,
            "name": stop.name,
            "x": stop.geolocation[0],
            "y": stop.geolocation[1],
            "time_to_other_stops": [
                {
                    "stop_id": stop_id,
                    "time_in_sec": time_to_other_stop.seconds
                } for stop_id, time_to_other_stop in stop.time_to_other_stops.items()

            ]

        } for stop in stops.values()]
        json_to_save = json.dumps(stops_to_save, indent=4)
        with open(self._file_name, "w+") as outfile:
            outfile.write(json_to_save)

    def add(self, name: str, geolocation_x: decimal, geolocation_y: decimal) -> Stop:
        new_stop = Stop(name=name,
                        geolocation=(geolocation_x, geolocation_y),
                        time_to_other_stops={},
                        id=str(uuid.uuid4()))
        stops = self._get_stops()
        stops[new_stop.id] = new_stop
        self._set_stops(stops)
        return new_stop

    def update(self, stop_id: str, updated_stop: Stop):
        stops = self._get_stops()
        stops[stop_id] = updated_stop
        self._set_stops(stops)

    def get(self, stop_id: str) -> Stop:
        return self._get_stops()[stop_id]

    def get_all(self) -> Set[Stop]:
        return {stop for stop in self._get_stops().values()}

    def get_many(self, stop_ids: set[str]) -> Set[Stop]:
        return {value for value in self._get_stops().values() if value.id in stop_ids}

    def set_time_between_stops(self, start_stop_id: str, end_stop_id: str, time: timedelta):
        stops = self._get_stops()
        start_stop = stops.get(start_stop_id)
        start_stop.time_to_other_stops[end_stop_id] = time
        stops[start_stop_id] = start_stop
        self._set_stops(stops)
