from typing import List

import falcon
from apispec import APISpec

from sustainerds.api.core import test_route as this_mod
from sustainerds.api.core.resource import BaseResource, ResourceContext
from sustainerds.api.core.route import SustainerdsRoute, add_routes


def include_routes_empty(app: falcon.API) -> List[SustainerdsRoute]:
    return []


def include_routes_good(app: falcon.API) -> List[SustainerdsRoute]:
    return [
        SustainerdsRoute("/user", BaseResource, "UserResource1"),
        SustainerdsRoute("/user2", BaseResource, "UserResource2"),
    ]


def test_add_routes(
    plain_test_app: falcon.API,
    plain_openapi_spec: APISpec,
    resource_ctx: ResourceContext,
):
    add_routes(
        plain_test_app,
        plain_openapi_spec,
        resource_ctx,
        this_mod,
        "include_routes_good",
    )
    add_routes(
        plain_test_app,
        plain_openapi_spec,
        resource_ctx,
        this_mod,
        "include_routes_empty",
    )

    assert len(plain_openapi_spec._paths) == 2
