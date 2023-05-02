from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, Integer, String
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
    # created_at = mapped_column(DateTime, default=datetime.now)
    # updated_at = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)


class Stop(Base):
    __tablename__ = "stop"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    loc_x: Mapped[int] = mapped_column(Integer, nullable=False)
    loc_y: Mapped[int] = mapped_column(Integer, nullable=False)


class StopTimes(Base):
    __tablename__ = "stop_times"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_stop_id: Mapped[int] = mapped_column(ForeignKey(Stop.id))
    end_stop_id: Mapped[int] = mapped_column(ForeignKey(Stop.id))
    time_in_seconds: Mapped[int] = mapped_column(Integer, nullable=False)


class Driver(Base):
    __tablename__ = "driver"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    pesel: Mapped[str] = mapped_column(String(11), nullable=False)
    phone: Mapped[str] = mapped_column(String(11), nullable=False)
    transits: Mapped[list["Transit"]] = relationship(back_populates="driver")


class RouteStop(Base):
    __tablename__ = "route_stop"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stop_id: Mapped[int] = mapped_column(Integer, ForeignKey(Stop.id))
    route_id: Mapped[int] = mapped_column(Integer, ForeignKey("route.id"))
    route: Mapped["Route"] = relationship(back_populates="stops")
    order: Mapped[int] = mapped_column(Integer)


class Route(Base):
    __tablename__ = "route"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    stops: Mapped[list[RouteStop]] = relationship( order_by=RouteStop.order, back_populates="route")
    transits: Mapped[list["Transit"]] = relationship(back_populates="route")


class Vehicle(Base):
    __tablename__ = "vehicle"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    capacity: Mapped[int] = mapped_column(Integer)
    transits: Mapped[list["Transit"]] = relationship( back_populates="vehicle")


class Transit(Base):
    '''
    Reason to use many to one
    https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#many-to-one
    '''
    __tablename__ = "transit"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    route_id: Mapped[int] = mapped_column(ForeignKey(Route.id))
    route: Mapped[Route] = relationship( back_populates="transits")
    start_time: Mapped[datetime] = mapped_column(DateTime)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey(Vehicle.id))
    vehicle: Mapped[Vehicle] = relationship( back_populates="transits")
    driver_id: Mapped[int] = mapped_column(ForeignKey(Driver.id))
    driver: Mapped[Driver] = relationship(back_populates="transits")
