from sustainerds.api.core.route import SustainerdsRoute, add_routes
from sustainerds.api.core.resource import SustainerdsResource
import sustainerds.api.core.test_route as this_mod
import falcon
from pytest import raises
from apispec import APISpec

def include_routes_empty(app):
    return []

def include_routes_good(app):
    return [
        SustainerdsRoute("/user", SustainerdsResource, {}),
        SustainerdsRoute("/user2", SustainerdsResource, {})
    ]

def include_routes_bad(app):
    return [
        SustainerdsRoute("/user", SustainerdsResource, {}),
        dict(aaa=123)
    ]

def test_add_routes(test_app: falcon.API, test_spec: APISpec):
    add_routes(test_app, test_spec, this_mod, 'include_routes_good')
    add_routes(test_app, test_spec, this_mod, 'include_routes_empty')

    with raises(ValueError):
        add_routes(test_app, test_spec, this_mod, 'include_routes_bad')

    assert len(test_spec._paths) == 2