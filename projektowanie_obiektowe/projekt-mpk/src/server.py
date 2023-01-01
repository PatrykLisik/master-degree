from sanic import Sanic, text

from src.web.backoffice_endpoints import backoffice_blueprint

app = Sanic("MPK")

app.blueprint(backoffice_blueprint)


@app.get("/")
async def hello_world(request):
    return text("Hello, world.")
