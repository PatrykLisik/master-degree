from sanic import Sanic, text

from src.web.driver_endpoints import backoffice_blueprint
from src.web.stop_endpoints import stop_blueprint

app = Sanic("MPK")

app.blueprint(backoffice_blueprint)
app.blueprint(stop_blueprint)


@app.get("/")
async def hello_world(request):
    return text("Hello, world.")
