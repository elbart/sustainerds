from dataclasses import dataclass
from typing import Dict, Optional, Type

from falcon import Request, Response
from marshmallow.schema import Schema
from marshmallow import fields

from sustainerds.api.core.resource import SustainerdsResource, RequestSchemaSpec, ResponseSchemaSpec, ResourceSchemaSpec, SchemaSpec, validate_schema
from sustainerds.api.entities.user.schemas import UserResponseSchema

class UserGetRequestSchema(RequestSchemaSpec):
    class Query(Schema):
        search = fields.Str(required=True)

    query = Query

class UserGetResponseSchema(ResponseSchemaSpec):
    json = UserResponseSchema


class UserResource(SustainerdsResource):

    schema_spec = ResourceSchemaSpec(
        GET=SchemaSpec(
            request=UserGetRequestSchema(),
            response=UserGetResponseSchema()
            )
    )

    @validate_schema()
    def on_get(self, req: Request, resp: Response):
        '''Get a user by user_id
        ---
        description: Get a Sustainerds User by Id
        responses:
            200:
                description: A Sustainerds User to be returned
                schema: UserResponseSchema
        '''
        user = {
            "email": "tim@elbart.com",
            "password": "bla123",
        }

        schema = UserResponseSchema()
        schema.load(user)

        resp.media = user
