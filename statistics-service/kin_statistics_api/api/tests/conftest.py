import pytest

from api.tests.settings import TestSettings
from config.containers import Container


@pytest.fixture()
def application():
    container = Container()
    container.config.from_pydantic(TestSettings())
    container.init_resources()

    yield container
