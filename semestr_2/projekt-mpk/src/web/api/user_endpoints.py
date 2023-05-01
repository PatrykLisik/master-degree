import json

from sanic import Blueprint, HTTPResponse, redirect, Request

from src.model.internal_model import User
from src.repositories.user_repository import AbstractUserRepository
from src.web.api import COOKIE_KEY
from src.web.api.user_usecase import create_app_user_usecase, login_user_usecase

user_blueprint = Blueprint(name="user", url_prefix="/user")


@user_blueprint.post("/create")
async def create_user(request: Request, user_repository: AbstractUserRepository) -> HTTPResponse:
    print(request.form)
    user = await create_app_user_usecase(
        user_repository=user_repository,
        email=request.form.get("email"),
        password=request.form.get("password"),
        name=request.form.get("name"),
    )
    response = redirect("/", )
    return add_logged_in_cookie(response, user)


@user_blueprint.post("/login")
async def login(request: Request, user_repository: AbstractUserRepository) -> HTTPResponse:
    print(request.form)
    user = await login_user_usecase(
        user_repository=user_repository,
        email=request.form.get("email"),
        password=request.form.get("password")
    )
    response = redirect("/", )
    return add_logged_in_cookie(response, user)


def add_logged_in_cookie(response: HTTPResponse, user: User) -> HTTPResponse:
    response.add_cookie(COOKIE_KEY, value=json.dumps({
        "name": user.name,
        "email": user.email,
        "id": user.id,
        "type": user.user_type.name
    },  separators=(',', ':')), secure=False, max_age=300)
    return response
