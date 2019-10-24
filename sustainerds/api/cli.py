from sustainerds.api.app import configure_app, create_app, create_openapi_spec
from sustainerds.api.core.persistence import InMemoryPersistence
from sustainerds.api.core.resource import ResourceContext


def print_spec():
    """Prints the OpenAPI specification of the full application"""
    app = create_app()
    spec = create_openapi_spec(app)
    ctx = ResourceContext(persistence=InMemoryPersistence())
    configure_app(app, spec, ctx)
    print(spec.to_yaml())
