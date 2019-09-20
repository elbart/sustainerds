from typing import Dict

from falcon import Request, Response
from marshmallow import fields
from marshmallow.schema import Schema

from sustainerds.api.core.resource import (
    BaseResource,
    RequestSchemaSpec,
    ResourceSchemaSpec,
    ResponseSchemaSpec,
    SchemaSpec,
)
from sustainerds.api.entities.user.model import User


class UserGetRequestSchema(RequestSchemaSpec):
    class Query(Schema):
        search = fields.Str()


class UserGetResponseSchema(ResponseSchemaSpec):
    class Json(Schema):
        id = fields.UUID()
        email = fields.Email()
        password = fields.Str()


class UserCollectionPostRequestSchema(RequestSchemaSpec):
    class Json(Schema):
        email = fields.Email(required=True)
        password = fields.Str(required=True)


class UserCollectionPostResponseSchema(ResponseSchemaSpec):
    class Json(Schema):
        id = fields.UUID(required=True)
        email = fields.Email(required=True)
        password = fields.Str(required=True)


class UserCollectionResource(BaseResource):
    """User collection resource"""

    @property
    def resource_schema_spec(self) -> ResourceSchemaSpec:
        return ResourceSchemaSpec(
            name="UserCollection",
            POST=SchemaSpec(
                request=UserCollectionPostRequestSchema(),
                response=UserCollectionPostResponseSchema(),
            ),
        )

    def on_post(self, req: Request, resp: Response):
        d: Dict = req.validated
        u = User(self.ctx.persistence)
        u.register(d["email"], d["password"])
        u.save()
        resp.media = u.to_dict()


class UserResource(BaseResource):
    """User resource"""

    @property
    def resource_schema_spec(self) -> ResourceSchemaSpec:
        return ResourceSchemaSpec(
            name="User",
            GET=SchemaSpec(
                request=UserGetRequestSchema(), response=UserGetResponseSchema()
            ),
        )

    def on_get(self, req: Request, resp: Response, user_id: str):
        """Get a user by user_id"""
        u = User(self.ctx.persistence)
        u.load(user_id)
        resp.media = u.to_dict()
