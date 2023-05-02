from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.model.database.model import User as DBUser, UserType as DBUserType
from src.model.domain_model import User, UserType
from src.repositories.abstract import AbstractUserRepository


class DatabaseUserRepository(AbstractUserRepository):

    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        self.session_maker = session_maker

    async def add(self, name: str, email: str, password_hash: str, user_type: UserType) -> User:
        async with self.session_maker() as session:
            async with session.begin():
                new_user = DBUser(
                    email_address=email,
                    name=name,
                    password_hash=password_hash,
                    user_type=DBUserType.Backoffice.name if user_type == UserType.Backoffice else DBUserType.App.name,
                )
                session.add(new_user)
                await session.flush()
                return User(
                    id=new_user.id,
                    name=new_user.name,
                    password_hash=new_user.password_hash,
                    user_type=user_type,
                    email=new_user.email_address
                )

    async def login(self, email: str, password_hash: str) -> User:
        async with self.session_maker() as session:
            stmt = select(DBUser).where(DBUser.email_address == email and DBUser.password_hash == password_hash)

            result = await session.execute(stmt)

            user = result.scalar()
            return User(
                id=user.id,
                name=user.name,
                password_hash=user.password_hash,
                user_type=UserType.Backoffice if user.user_type == DBUserType.Backoffice else UserType.App,
                email=user.email_address
            )
