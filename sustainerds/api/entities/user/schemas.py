import uuid

from marshmallow import Schema, fields


class UserResponseSchema(Schema):
    id = fields.UUID(missing=uuid.uuid4)
    email = fields.Email()
    password = fields.Str()
