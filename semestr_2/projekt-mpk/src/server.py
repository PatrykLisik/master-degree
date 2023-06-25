import os

from sanic import Sanic

from src.model.database.connection import async_session_maker
from src.repositories.abstract import (
    AbstractRouteRepository,
    AbstractStopRepository,
    AbstractTransitRepository,
    AbstractUserRepository,
)
from src.repositories.route_repository import InFileRouteRepository, DatabaseRouteRepository
from src.repositories.stop_repository import InFileStopRepository, DatabaseStopRepository
from src.repositories.transit_repository import InFileTransitRepository, DatabaseTransitRepository
from src.repositories.user_repository import DatabaseUserRepository
from src.web.api.frontend_enpoints import html_blueprint
from src.web.api.mobile_app_endpoints import mobile_app_blueprint
from src.web.api.route_endpoint import route_blueprint
from src.web.api.stop_endpoints import stop_blueprint
from src.web.api.transit_endpoints import transit_blueprint
from src.web.api.user_endpoints import user_blueprint


app = Sanic("MPK")
app.config.TEMPLATING_PATH_TO_TEMPLATES = os.getenv(
    "TEMPLATING_PATH_TO_TEMPLATES", "templates"
)
app.config.INJECTION_SIGNAL = "http.handler.before"


app.blueprint(stop_blueprint)
app.blueprint(route_blueprint)

app.blueprint(transit_blueprint)
app.blueprint(mobile_app_blueprint)
app.blueprint(html_blueprint)
app.blueprint(user_blueprint)

app.ext.add_dependency(
    AbstractUserRepository,
    lambda: DatabaseUserRepository(session_maker=async_session_maker),
)


app.ext.add_dependency(AbstractStopRepository, lambda: DatabaseStopRepository(session_maker=async_session_maker))
app.ext.add_dependency(AbstractRouteRepository, lambda: DatabaseRouteRepository(session_maker=async_session_maker))
app.ext.add_dependency(AbstractTransitRepository, lambda: DatabaseTransitRepository(session_maker=async_session_maker))

if __name__ == "__main__":
    app.run(port=8080, dev=True)
