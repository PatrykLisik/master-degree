import os

import pytest


@pytest.hookimpl(tryfirst=True)
def pytest_load_initial_conftests(args, early_config, parser):
    os.environ["DB_HOST"] = "db"
