import json

from sanic import Blueprint, HTTPResponse, Request
from sanic.log import logger
from sanic_ext import render

from src.web.api import COOKIE_KEY

html_blueprint = Blueprint(name="frontend", url_prefix="/")


@html_blueprint.get("/")
async def index(request: Request) -> HTTPResponse:
    user_data = request.cookies.get(COOKIE_KEY, {})
    if user_data:
        user_data = json.loads(user_data)
    logger.debug(f"Cookie {user_data}")
    return await render(
        "browse_lines.html", status=200, context={"user_data": user_data}
    )


@html_blueprint.get("/login")
async def login(request: Request) -> HTTPResponse:
    return await render("login.html", status=200)


@html_blueprint.get("/signup")
async def signup(request: Request) -> HTTPResponse:
    return await render("signup.html", status=200)
