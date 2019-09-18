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
from sustainerds.api.entities.user.schemas import UserResponseSchema


class UserGetRequestSchema(RequestSchemaSpec):
    class Query(Schema):
        search = fields.Str(required=True)

    query = Query


class UserGetResponseSchema(ResponseSchemaSpec):
    json = UserResponseSchema


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

        schema = UserResponseSchema()
        schema.load(user)

        resp.media = user
