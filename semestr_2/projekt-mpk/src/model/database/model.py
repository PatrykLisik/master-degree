import decimal
from datetime import datetime, time
from enum import Enum

from sqlalchemy import DateTime, DECIMAL, ForeignKey, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.database import Base


class UserType(Enum):
    App = 1
    Backoffice = 2


class User(Base):
    __tablename__ = "app_user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email_address: Mapped[str] = mapped_column(String(60), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    user_type: Mapped[UserType] = mapped_column(String(60))


class Stop(Base):
    __tablename__ = "stop"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    loc_x: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 5), nullable=False)
    loc_y: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 5), nullable=False)
    route_stops: Mapped[list["RouteStop"]] = relationship(back_populates="stop")
    stop_times: Mapped[list["StopTimes"]] = relationship(
        back_populates="start_stop",
        foreign_keys="StopTimes.start_stop_id",
        lazy="joined",
        passive_deletes=True,
    )


class StopTimes(Base):
    __tablename__ = "stop_times"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_stop_id: Mapped[int] = mapped_column(
        ForeignKey(Stop.id, ondelete="CASCADE", onupdate="CASCADE"),
    )
    start_stop: Mapped["Stop"] = relationship(
        back_populates="stop_times",
        foreign_keys="StopTimes.start_stop_id",
    )
    end_stop_id: Mapped[int] = mapped_column(ForeignKey(Stop.id))
    time_in_seconds: Mapped[int] = mapped_column(Integer, nullable=False)


class RouteStop(Base):
    __tablename__ = "route_stop"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stop_id: Mapped[int] = mapped_column(Integer, ForeignKey(Stop.id))
    stop: Mapped[Stop] = relationship(back_populates="route_stops")
    route_id: Mapped[int] = mapped_column(Integer, ForeignKey("route.id"))
    route: Mapped["Route"] = relationship(back_populates="stops")
    order: Mapped[int] = mapped_column(Integer)


class Route(Base):
    __tablename__ = "route"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    stops: Mapped[list[RouteStop]] = relationship(
        order_by=RouteStop.order,
        back_populates="route",
        lazy="joined",
        passive_deletes=True,
    )
    transits: Mapped[list["Transit"]] = relationship(
        back_populates="route",
        lazy="joined",
        passive_deletes=True,
    )


class Transit(Base):
    """
    Reason to use many to one
    https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#many-to-one
    """

    __tablename__ = "transit"

    id: Mapped[int] = mapped_column(Integer,
                                    primary_key=True)
    route_id: Mapped[int] = mapped_column(ForeignKey(Route.id))
    route: Mapped[Route] = relationship(back_populates="transits")
    start_time: Mapped[time] = mapped_column(Time)
