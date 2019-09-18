import uuid

from falcon import Request, Response
from marshmallow import fields
from marshmallow.schema import Schema

from sustainerds.api.core.resource import (
    RequestSchemaSpec,
    ResourceSchemaSpec,
    ResponseSchemaSpec,
    SchemaSpec,
    SustainerdsResource,
)


class UserGetRequestSchema(RequestSchemaSpec):
    class Query(Schema):
        search = fields.Str()


class UserGetResponseSchema(ResponseSchemaSpec):
    class Json(Schema):
        id = fields.UUID(missing=uuid.uuid4)
        email = fields.Email()
        password = fields.Str()


class UserResource(SustainerdsResource):
    """User collection resource"""

    @property
    def resource_schema_spec(self) -> ResourceSchemaSpec:
        return ResourceSchemaSpec(
            name="UserCollection",
            GET=SchemaSpec(
                request=UserGetRequestSchema(), response=UserGetResponseSchema()
            ),
        )

    def on_get(self, req: Request, resp: Response):
        """Get a user by user_id"""
        user = {"email": "tim@elbart.com", "password": "bla123"}

        resp.media = user
