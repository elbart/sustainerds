import falcon
from apispec import APISpec
from pytest import raises

from sustainerds.api.core import test_route as this_mod
from sustainerds.api.core.resource import BaseResource
from sustainerds.api.core.route import SustainerdsRoute, add_routes


def include_routes_empty(app):
    return []


def include_routes_good(app):
    return [
        SustainerdsRoute("/user", BaseResource, {}),
        SustainerdsRoute("/user2", BaseResource, {}),
    ]


def include_routes_bad(app):
    return [SustainerdsRoute("/user", BaseResource, {}), dict(aaa=123)]


def test_add_routes(test_app: falcon.API, plain_openapi_spec: APISpec):
    add_routes(test_app, plain_openapi_spec, this_mod, "include_routes_good")
    add_routes(test_app, plain_openapi_spec, this_mod, "include_routes_empty")

    with raises(ValueError):
        add_routes(test_app, plain_openapi_spec, this_mod, "include_routes_bad")

    assert len(plain_openapi_spec._paths) == 2
