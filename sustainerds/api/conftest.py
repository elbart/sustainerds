import falcon
import pytest
from apispec import APISpec
from falcon import testing

from sustainerds.api.app import configure_app, create_app, create_openapi_spec
from sustainerds.api.core.persistence import InMemoryPersistence
from sustainerds.api.core.resource import ResourceContext


@pytest.fixture()
def resource_ctx():
    return ResourceContext(persistence=InMemoryPersistence())


@pytest.fixture
def plain_test_app() -> falcon.API:
    return create_app()


@pytest.fixture
def plain_openapi_spec(plain_test_app: falcon.API) -> APISpec:
    return create_openapi_spec(plain_test_app)


@pytest.fixture
def test_app(
    plain_test_app: falcon.API,
    plain_openapi_spec: APISpec,
    resource_ctx: ResourceContext,
) -> falcon.API:
    configure_app(plain_test_app, plain_openapi_spec, resource_ctx)

    return plain_test_app


@pytest.fixture
def test_client(test_app):
    # Assume the hypothetical `myapp` package has a function called
    # `create()` to initialize and return a `falcon.API` instance.
    return testing.TestClient(test_app)
