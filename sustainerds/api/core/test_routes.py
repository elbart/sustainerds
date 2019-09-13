from sustainerds.api.core.routes import SustainerdsRoute, add_routes
from sustainerds.api.core.resource import SustainerdResource
from sustainerds.api.core.routes import add_routes
import sustainerds.api.core.test_routes as this_mod
import falcon
from pytest import raises

def include_routes_empty(app):
    return []

def include_routes_good(app):
    return [
        SustainerdsRoute("/user", SustainerdResource(), {})
    ]

def include_routes_bad(app):
    return [
        SustainerdsRoute("/user", SustainerdResource(), {}),
        dict(aaa=123)
    ]

def test_add_routes(test_app: falcon.API):
    add_routes(test_app, this_mod, 'include_routes_good')
    add_routes(test_app, this_mod, 'include_routes_empty')

    with raises(ValueError):
        add_routes(test_app, this_mod, 'include_routes_bad')