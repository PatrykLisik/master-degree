from sanic import Sanic, text

from src.web.driver_endpoints import driver_blueprint
from src.web.mobile_app_endpoints import mobile_app_blueprint
from src.web.route_endpoint import route_blueprint
from src.web.stop_endpoints import stop_blueprint
from src.web.transit_endpoints import transit_blueprint
from src.web.vehicle_enpoints import vehicle_blueprint

app = Sanic("MPK")

app.blueprint(driver_blueprint)
app.blueprint(stop_blueprint)
app.blueprint(route_blueprint)
app.blueprint(vehicle_blueprint)
app.blueprint(transit_blueprint)
app.blueprint(mobile_app_blueprint)


@app.get("/")
async def hello_world(request):
    return text("Hello, world.")
