import os

from sanic import Sanic

from src.database.connection import async_session_maker
from src.repositories.user_repository import AbstractUserRepository, DatabaseUserRepository
from src.web.api.driver_endpoints import driver_blueprint
from src.web.api.frontend_enpoints import html_blueprint
from src.web.api.mobile_app_endpoints import mobile_app_blueprint
from src.web.api.route_endpoint import route_blueprint
from src.web.api.stop_endpoints import stop_blueprint
from src.web.api.transit_endpoints import transit_blueprint
from src.web.api.user_endpoints import user_blueprint
from src.web.api.vehicle_enpoints import vehicle_blueprint

app = Sanic("MPK")
app.config.TEMPLATING_PATH_TO_TEMPLATES = os.getenv("TEMPLATING_PATH_TO_TEMPLATES", "templates")
app.config.INJECTION_SIGNAL = "http.handler.before"

app.blueprint(driver_blueprint)
app.blueprint(stop_blueprint)
app.blueprint(route_blueprint)
app.blueprint(vehicle_blueprint)
app.blueprint(transit_blueprint)
app.blueprint(mobile_app_blueprint)
app.blueprint(html_blueprint)
app.blueprint(user_blueprint)

app.ext.add_dependency(AbstractUserRepository, lambda: DatabaseUserRepository(session_maker=async_session_maker))

if __name__ == '__main__':
    app.run(port=8080, dev=True)
