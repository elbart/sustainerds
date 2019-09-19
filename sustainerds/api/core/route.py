from dataclasses import dataclass
from types import ModuleType
from typing import Dict, Optional, Text, Type

import falcon
from apispec import APISpec

from sustainerds.api.core.openapi import add_openapi_specs
from sustainerds.api.core.resource import BaseResource


@dataclass
class SustainerdsRoute:
    """ Represents a route which we can define and return in our entities """

    path: str
    resource: Type[BaseResource]
    name: Text
    kwargs: Optional[Dict] = None


def add_routes(
    app: falcon.API, openapi_spec: APISpec, mod: ModuleType, fname: Optional[str] = None
):
    """
    Looks up the `include_routes` callable within the
    passed module and executes the callable. The result
    of the callable is exepected to be of type `List[SustainerdsRoute]`.
    The list is iterated and each individual resource is added to the falcon app.
    """
    fn = getattr(mod, fname if fname else "include_routes")
    if fn:
        for r in fn(app):
            if not isinstance(r, SustainerdsRoute):
                raise ValueError(
                    f"Object {r} required to be of type SustainerdsRoute, but was {type(r)}. Imported from module {mod}"
                )
            resource: BaseResource = r.resource(app, r.name)
            # resource.resource_schema_spec

            if not r.kwargs:
                r.kwargs = {}

            app.add_route(r.path, resource, **r.kwargs)
            add_openapi_specs(openapi_spec, r.path, resource, r.name)
