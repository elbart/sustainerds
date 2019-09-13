import pytest
import falcon

@pytest.fixture
def test_app() -> falcon.API:
    return falcon.API()