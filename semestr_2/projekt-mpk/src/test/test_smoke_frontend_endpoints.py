import pytest


class StopsTestFacade:

    def __init__(self, test_cli):
        self.test_cli = test_cli

    async def get_stops_page_content(self):
        response = self.test_cli.get("/bus-stops")
        return response


# @pytest.fixture
# def stops_facade(test_cli):
#     yield StopsTestFacade(test_cli=app)


@pytest.mark.asyncio
async def test_get_stops_with_no_data(app):
    response = await app.get("/bus-stops")
    assert response


@pytest.mark.asyncio
async def test_get_browse_lines_with_no_data(app):
    response = await app.get("/browse-lines/")
    assert response


@pytest.mark.asyncio
async def test_get_browse_lines_with_line(app):
    response = await app.get("/browse-lines/1")
    assert response


@pytest.mark.asyncio
async def test_get_browse_lines_with_line_and_stop(app):
    response = await app.get("/browse-lines/1/1/")
    assert response


@pytest.mark.asyncio
async def test_get_bus_stops_with_no_data(app):
    response = await app.get("/bus-stops")
    assert response


@pytest.mark.asyncio
async def test_login(app):
    response = await app.get("/login")
    assert response


@pytest.mark.asyncio
async def test_signup(app):
    response = await app.get("/signup")
    assert response


@pytest.mark.asyncio
async def test_get_bus_stops_with_selected_stop(app):
    response = await app.get("/bus-stops?selected_stop=1")
    assert response


@pytest.mark.asyncio
async def test_get_bus_stops_with_selected_stop_and_target_stop(app):
    response = await app.get("/bus-stops?selected_stop=1&target_stop=2")
    assert response


@pytest.mark.asyncio
async def test_get_signup_with_no_data(app):
    response = await app.get("/signup")
    assert response


@pytest.mark.asyncio
async def test_edit_line_2_with_no_data(app):
    response = await app.get("/edit-line/2")
    assert response


@pytest.mark.asyncio
async def test_edit_line_transits_2_with_no_data(app):
    response = await app.get("/edit-line-transits/2")
    assert response


@pytest.mark.asyncio
async def test_bus_lines(app):
    response = await app.get("/bus-lines")
    assert response


@pytest.mark.asyncio
async def test_logout(app):
    response = await app.get("/logout")
    assert response


@pytest.mark.asyncio
async def test_logout(app):
    response = await app.get("/api/bus-stops/search?query=12")
    assert response
