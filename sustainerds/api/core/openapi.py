from typing import Text

from apispec import APISpec

from sustainerds.api.core.resource import SustainerdsResource


def add_openapi_specs(o: APISpec, path: str, resource: SustainerdsResource, name: Text):
    o.path(path=path, operations={})

    # openapi_spec.components.schema(r.name, schema=)
