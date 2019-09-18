from marshmallow import Schema, fields
import uuid

class UserResponseSchema(Schema):
    id = fields.UUID(missing=uuid.uuid4)
    email = fields.Email()
    password = fields.Str()