from dataclasses import dataclass, field
from datetime import timedelta, time
from enum import Enum
from itertools import pairwise
from typing import Self

from sanic.log import logger


@dataclass(frozen=True)
class Stop:
    id: str = field(hash=True)
    name: str = field(hash=False)
    loc_x: str = field(hash=False)
    loc_y: str = field(hash=False)
    time_to_other_stops: dict[Self, timedelta] = field(hash=False, default_factory=dict)


@dataclass(frozen=True)
class Route:
    id: str = field(hash=True)
    name: str = field(hash=True)
    stops: list[Stop] = field(hash=False)
    transits: list["Transit"] = field(hash=False, default_factory=list)

    @property
    def combined_time(self) -> timedelta:
        combined_time = timedelta()
        # logger.debug(f"self.stops {self.stops}")
        for start_stop, next_stop in pairwise(self.stops):
            # logger.debug(f"Start_stop {start_stop} | next_stop {next_stop}")
            if start_stop and next_stop:
                time_to_next_stop = start_stop.time_to_other_stops.get(str(next_stop.id), timedelta())
                combined_time += time_to_next_stop
        return combined_time


@dataclass(frozen=True)
class Transit:
    id: str = field(hash=True)
    route: Route = field(hash=False)
    start_time: time = field(hash=False)


class UserType(Enum):
    App = 1
    Backoffice = 2


@dataclass(frozen=True)
class User:
    id: str = field(hash=True)
    name: str = field(hash=False)
    email: str = field(hash=False)
    password_hash: str = field(hash=False)
    user_type: UserType = field(hash=False)
