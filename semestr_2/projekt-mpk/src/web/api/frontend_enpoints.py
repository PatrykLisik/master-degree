from sanic import json, Blueprint, HTTPResponse
from sanic_ext import render

html_blueprint = Blueprint(name="frontend", url_prefix="/")


@html_blueprint.get("/")
async def index(request) -> HTTPResponse:
    return await render("welcome.html", status=200)


@html_blueprint.get("/login")
async def index(request) -> HTTPResponse:
    return await render("login.html", status=200)
