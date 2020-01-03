import falcon
from apispec import APISpec
from marshmallow import Schema, fields

from sustainerds.api.core.openapi import add_openapi_specs
from sustainerds.api.core.resource import (
    BaseResource,
    RequestSchemaSpec,
    ResourceSchemaSpec,
    ResponseSchemaSpec,
    SchemaSpec,
)


class ATestResourceGetResponseSchema(ResponseSchemaSpec):
    class Json(Schema):
        email = fields.Email(required=True)
        password = fields.String()


class ATestResourcePostRequestSchema(RequestSchemaSpec):
    class Json(Schema):
        id = fields.UUID(required=True)
        email = fields.Email(required=True)
        password = fields.String(required=True)


class PathSchema(Schema):
    user_id = fields.UUID(required=True)


class ATestResource(BaseResource):
    @property
    def resource_schema_spec(self) -> ResourceSchemaSpec:

        return ResourceSchemaSpec(
            name="TestResource",
            path=PathSchema(),
            GET=SchemaSpec(
                request=RequestSchemaSpec(), response=ATestResourceGetResponseSchema()
            ),
            POST=SchemaSpec(
                request=ATestResourcePostRequestSchema(), response=ResponseSchemaSpec()
            ),
        )


def test_openapi_paths(plain_test_app: falcon.API, plain_openapi_spec: APISpec):
    add_openapi_specs(
        plain_openapi_spec,
        "/test/{user_id}",
        ATestResource(plain_test_app, "TestResource"),
    )

    assert len(plain_openapi_spec.components._schemas) == 2
    assert "ATestResourceGetResponseSchema" in plain_openapi_spec.components._schemas
    assert "ATestResourcePostRequestSchema" in plain_openapi_spec.components._schemas
    assert "/test/{user_id}" in plain_openapi_spec._paths
    assert "responses" in plain_openapi_spec._paths["/test/{user_id}"]["get"]
    assert "parameters" in plain_openapi_spec._paths["/test/{user_id}"]
    assert len(plain_openapi_spec._paths["/test/{user_id}"]["parameters"]) == 1

    assert (
        plain_openapi_spec._paths["/test/{user_id}"]["parameters"][0]["name"]
        == "user_id"
    )
    assert plain_openapi_spec._paths["/test/{user_id}"]["parameters"][0]["in"] == "path"
    assert (
        plain_openapi_spec._paths["/test/{user_id}"]["parameters"][0]["required"]
        == True
    )
    assert (
        plain_openapi_spec._paths["/test/{user_id}"]["parameters"][0]["schema"]["type"]
        == "string"
    )

    assert plain_openapi_spec._paths["/test/{user_id}"]["get"]["responses"]["200"] == {
        "content": {
            "application/json": {
                "schema": {"$ref": "#/components/schemas/ATestResourceGetResponseSchema"}
            }
        },
        "description": "",
    }
    assert "requestBody" in plain_openapi_spec._paths["/test/{user_id}"]["post"]
    assert (
        plain_openapi_spec._paths["/test/{user_id}"]["post"]["requestBody"]
        == "#/components/schemas/ATestResourcePostRequestSchema"
    )
