"""create mpk model

Revision ID: e196dabe7eb2
Revises: 8f6883b3c098
Create Date: 2023-05-02 15:21:19.245772

"""
from alembic import op
from sqlalchemy import (
    Column,
    DateTime,
    DECIMAL, ForeignKey,
    Integer,
    PrimaryKeyConstraint,
    String,
)

# revision identifiers, used by Alembic.
revision = "e196dabe7eb2"
down_revision = "8f6883b3c098"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "stop",
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("name", String(length=50), nullable=False),
        Column("loc_x", DECIMAL(3, 5), nullable=False),
        Column("loc_y", DECIMAL(3, 5)),
        PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "stop_times",
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column(
            "start_stop_id", Integer, ForeignKey("stop.id", name="stop_times_start_id")
        ),
        Column("end_stop_id", Integer, ForeignKey("stop.id", name="stop_times_end_id")),
        Column("time_in_seconds", Integer),
        PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "driver",
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("first_name", String(length=50), nullable=False),
        Column("last_name", String(length=50), nullable=False),
        Column("pesel", String(length=11), nullable=False),
        Column("phone", String(length=11), nullable=False),
        PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "route",
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("name", String(length=50), nullable=False),
        PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "vehicle",
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("capacity", Integer, nullable=False),
        PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "route_stop",
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("start_stop_id", Integer, ForeignKey("stop.id")),
        Column("route_id", Integer, ForeignKey("route.id")),
        Column("order", Integer, nullable=False),
        PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "transit",
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("route_id", Integer, ForeignKey("route.id")),
        Column("vehicle_id", Integer, ForeignKey("vehicle.id")),
        Column("driver_id", Integer, ForeignKey("driver.id")),
        Column("start_time", DateTime, nullable=False),
        PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    pass
