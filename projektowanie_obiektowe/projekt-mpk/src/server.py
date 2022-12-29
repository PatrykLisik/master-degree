from sanic import Sanic, text

app = Sanic("mpk")


@app.get("/")
async def hello_world(request):
    return text("Hello, world.")

