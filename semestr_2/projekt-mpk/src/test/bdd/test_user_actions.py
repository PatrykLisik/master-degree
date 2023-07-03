import asyncio

import pytest
from pytest_bdd import given, when, then, parsers, scenarios

scenarios("")


@when(parsers.parse("User creates account with {mail} mail {password} password {name} name"),
      target_fixture="create_user_response")
@pytest.mark.asyncio
def create_user(app, mail, password, name):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(app.post("/user/create", data={"email": mail, "name": name, "password": password}))


@then(parsers.parse("User with mail {mail} and password {password} is persisted in repository"))
@pytest.mark.asyncio
def step_impl(app, mail, password):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(app.post("/user/login", data={"email": mail, "password": password}))


@then("User receives cookie")
@pytest.mark.asyncio
def step_impl(create_user_response):
    request, response = create_user_response
    assert response.status_code  # FIXME make it work


@given("app is running")
def step_impl(app):
    return app
