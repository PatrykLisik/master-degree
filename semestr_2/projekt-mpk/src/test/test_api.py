import pytest


@pytest.mark.asyncio
async def test_bus_line_search(app):
    response = await app.get("/api/lines-search?query=test")
    assert response


@pytest.mark.asyncio
async def test_bus_line_stop_search(app):
    response = await app.get("/api/bus-stops?query=test")
    assert response


@pytest.mark.asyncio
async def test_bus_line_add(app):
    response = await app.post("/api/line-add",
                              json={"name": "test123"})
    assert response


@pytest.mark.asyncio
async def test_transit_add(app):
    response = await app.post("/api/transit-add",
                              json={"line_id": 1, "start_time": "15:10"})
    assert response


@pytest.mark.asyncio
async def test_save_distance_data(app):
    response = await app.post("/api/set-times-between-stops",
                              json={"stop_id": 1, "other_stop_id": 2, "time": 15})
    assert response
    await app.delete("/api/bus-stops/1/distance/2")


@pytest.mark.asyncio
async def test_get_distance_data(app):
    response = await app.post("/api/bus-stops/1/distances")
    assert response


@pytest.mark.asyncio
@pytest.mark.skip
async def test_delete_bus_line(app):
    await app.post("/api/line-add",
                   json={"name": "test123"})
    _, response_search = await app.get("/api/bus-stops?query=test123")
    line_id = response_search.json()[0]["id"]
    print(f"XXX line_id {line_id}")
    response = await app.delete(f"/api/bus-line/{line_id}")
    assert response
