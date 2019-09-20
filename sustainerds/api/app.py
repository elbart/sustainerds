import falcon
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

from sustainerds.api.core.persistence import InMemoryPersistence
from sustainerds.api.core.resource import ResourceContext, SchemaValidatorComponent
from sustainerds.api.core.route import add_routes
from sustainerds.api.entities import user


# from falcon_apispec import FalconPlugin


def create_app(sqla_session=None) -> falcon.API:
    """Creates the falcon app and takes the respective arguments we need:
    - database
    - filesystem
    - configuration
    - etc.
    """
    # Create Falcon web app
    app = falcon.API(middleware=[SchemaValidatorComponent()])
    return app


def create_openapi_spec(app: falcon.API) -> APISpec:
    """Creates an OpenAPI Spec for the Sustainerds API"""
    spec = APISpec(
        title="Sustainerds API",
        version="1.0.0",
        openapi_version="3.0.0",
        plugins=[MarshmallowPlugin()],
    )
    return spec


def configure_app(app: falcon.API, spec: APISpec, ctx: ResourceContext):
    add_routes(app, spec, ctx, user)


def get_app() -> falcon.API:
    """The actual wsgi application factory which is stitching all the
    required things together"""
    app = create_app()
    spec = create_openapi_spec(app)
    ctx = ResourceContext(persistence=InMemoryPersistence())
    configure_app(app, spec, ctx)
    print(spec.to_yaml())

    return app
