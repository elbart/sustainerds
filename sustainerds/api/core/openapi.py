from typing import Dict, Text, Type

from apispec import APISpec

from sustainerds.api.core.resource import BaseResource


def add_openapi_specs(o: APISpec, path: str, resource: BaseResource):
    """Add the resources specifcations to the api sepc object"""

    operations: Dict = dict()

    methods = resource.resource_schema_spec.get_methods()

    for method, spec in methods:

        if spec.request:
            if spec.request.json:
                schema_name = f"{type(spec.request).__name__}"
                o.components.schema(schema_name, schema=spec.request.json)

                operations[method.lower()] = dict(
                    summary="", requestBody=f"#/components/schemas/{schema_name}"
                )

            # TODO: get it to work. Currently I get this error.
            # ValueError: [{'in': 'query', 'schema': <Query(many=False)>}] doesn't have either `fields` or `_declared_fields`.
            # if spec.request.query:
            #     oa = OpenAPIConverter('3.0.0', lambda x: x, o)
            #     operations['parameters'] = oa.schema2parameters([
            #         {"in": "query", "schema": spec.request.query()}
            #     ])

        if spec.response and spec.response.json:
            schema_name = f"{type(spec.response).__name__}"
            o.components.schema(schema_name, schema=spec.response.json)

            operations.setdefault(method.lower(), dict())
            operations[method.lower()] = {
                "responses": {
                    "200": {
                        "description": "",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": f"#/components/schemas/{schema_name}"
                                }
                            }
                        },
                    }
                }
            }

    o.path(path=path, operations=operations)
