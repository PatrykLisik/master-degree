from dataclasses import asdict

from sanic import json, Blueprint
from sanic_ext import render

html_blueprint = Blueprint(name="frontend", url_prefix="/")


@html_blueprint.get("/")
async def index(request):
    return await render("index.html", context={"test_str": "test123"}, status=200)
