from datetime import time

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.model.database.model import Transit as DBTransit
from src.repositories.abstract import (
    AbstractTransitRepository,
)


class DatabaseTransitRepository(AbstractTransitRepository):
    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        self.session_maker = session_maker

    async def add(self, route_id: str, start_time: time):
        async with self.session_maker() as session:
            new_transit = DBTransit(start_time=start_time, route_id=int(route_id))
            session.add(new_transit)
            await session.commit()

    async def delete(self, transit_id: str):
        async with self.session_maker() as session:
            delete_stop_statement = delete(DBTransit).where(
                DBTransit.id == int(transit_id)
            )
            await session.execute(delete_stop_statement)
            await session.commit()
