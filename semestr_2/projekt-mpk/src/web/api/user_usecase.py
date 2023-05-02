from hashlib import sha256

from src.model.domain_model import UserType
from src.repositories.abstract import AbstractUserRepository


async def create_app_user_usecase(
    user_repository: AbstractUserRepository, name: str, email: str, password: str
):
    new_user = await user_repository.add(
        name=name,
        email=email,
        password_hash=sha256(password.encode()).hexdigest(),
        user_type=UserType.App,
    )
    return new_user


async def login_user_usecase(
    user_repository: AbstractUserRepository, email: str, password: str
):
    user = await user_repository.login(
        email=email,
        password_hash=sha256(password.encode()).hexdigest(),
    )
    return user
