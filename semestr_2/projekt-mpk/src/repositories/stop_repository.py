import decimal
import json
import uuid
from datetime import timedelta
from typing import Dict, Set

from sanic.log import logger

from src.model.domain_model import Stop as DomainStop
from src.model.infile_mappers import infile_stop_to_domain
from src.model.infile_model import Stop
from src.repositories.abstract import AbstractStopRepository


class InMemoryStopRepository(AbstractStopRepository):
    _stops: dict[str, Stop] = {}

    def add(self, name: str, geolocation_x: decimal, geolocation_y: decimal) -> DomainStop:
        new_stop = Stop(name=name,
                        geolocation=(geolocation_x, geolocation_y),
                        time_to_other_stops_in_seconds={},
                        id=str(uuid.uuid4()))
        self._stops[new_stop.id] = new_stop
        return infile_stop_to_domain(new_stop)

    def update(self, stop_id: str, updated_stop: DomainStop):
        self._stops[stop_id] = updated_stop

    def get(self, stop_id: str) -> DomainStop:
        return infile_stop_to_domain(self._stops[stop_id])

    def get_all(self) -> Set[DomainStop]:
        return {infile_stop_to_domain(stop) for stop in self._stops.values()}

    def get_many(self, stop_ids: set[str]) -> Set[DomainStop]:
        return {infile_stop_to_domain(value) for value in self._stops.values() if value.id in stop_ids}

    def set_time_between_stops(self, start_stop_id: str, end_stop_id: str, time: timedelta):
        start_stop = self._stops.get(start_stop_id)
        start_stop.time_to_other_stops_in_seconds[end_stop_id] = time.seconds


class InFileStopRepository(AbstractStopRepository):
    _file_name = "data/stop.json"

    def _get_stops(self) -> Dict[str, Stop]:

        try:
            with open(self._file_name, "r+", ) as infile:
                logger.info("load stops")
                data = json.load(infile)
                return {stop_data["id"]: Stop(
                    id=stop_data["id"],
                    name=stop_data["name"],
                    geolocation=(stop_data["x"], stop_data["y"]),
                    time_to_other_stops_in_seconds={times["stop_id"]: int(times["time_in_sec"])
                                                    for times in stop_data["time_to_other_stops_in_seconds"]}
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
            "time_to_other_stops_in_seconds": [
                {
                    "stop_id": stop_id,
                    "time_in_sec": time_to_other_stop
                } for stop_id, time_to_other_stop in stop.time_to_other_stops_in_seconds.items()

            ]

        } for stop in stops.values()]
        json_to_save = json.dumps(stops_to_save, indent=4)
        with open(self._file_name, "w+") as outfile:
            outfile.write(json_to_save)

    async def add(self, name: str, geolocation_x: decimal, geolocation_y: decimal) -> Stop:
        new_stop = Stop(name=name,
                        geolocation=(geolocation_x, geolocation_y),
                        time_to_other_stops_in_seconds={},
                        id=str(uuid.uuid4()))
        stops = self._get_stops()
        stops[new_stop.id] = new_stop
        self._set_stops(stops)
        return infile_stop_to_domain(new_stop)

    async def update(self, stop_id: str, updated_stop: Stop):
        stops = self._get_stops()
        stops[stop_id] = updated_stop
        self._set_stops(stops)

    async def get(self, stop_id: str) -> Stop:
        return infile_stop_to_domain(self._get_stops()[stop_id])

    async def get_all(self) -> Set[Stop]:
        return {infile_stop_to_domain(stop) for stop in self._get_stops().values()}

    async def get_many(self, stop_ids: set[str]) -> Set[Stop]:
        return {infile_stop_to_domain(value) for value in self._get_stops().values() if value.id in stop_ids}

    async def set_time_between_stops(self, start_stop_id: str, end_stop_id: str, time: timedelta):
        stops = self._get_stops()
        start_stop = stops.get(start_stop_id)
        start_stop.time_to_other_stops_in_seconds[end_stop_id] = time.seconds
        stops[start_stop_id] = start_stop
        self._set_stops(stops)
