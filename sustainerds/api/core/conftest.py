import falcon
import pytest
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from falcon_apispec import FalconPlugin


@pytest.fixture
def test_app() -> falcon.API:
    return falcon.API()


@pytest.fixture
def test_spec(test_app) -> APISpec:
    # Create an APISpec
    spec = APISpec(
        title="Test API Spec",
        version="1.0.0",
        openapi_version="3.0",
        plugins=[FalconPlugin(test_app), MarshmallowPlugin()],
    )

    return spec
