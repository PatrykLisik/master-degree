import pytest
from sanic_testing import TestManager

from src.server import create_app


@pytest.fixture
def app():
    app = create_app("TestMPK")
    TestManager(app)
    yield app.asgi_client
