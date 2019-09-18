from dataclasses import dataclass
from typing import Optional, Type

import falcon
from marshmallow.schema import Schema


@dataclass
class RequestSchemaSpec:
    '''Schema definition wrapper to cover all different locations to check for input data on the request'''
    query: Optional[Type[Schema]] = None
    json: Optional[Type[Schema]] = None
    headers: Optional[Type[Schema]] = None
    cookies: Optional[Type[Schema]] = None
    form: Optional[Type[Schema]] = None


@dataclass
class ResponseSchemaSpec:
    '''Schema definition wrapper to cover all different locations to check for output data on the response'''
    json: Optional[Type[Schema]] = None
    headers: Optional[Type[Schema]] = None


@dataclass
class SchemaSpec:
    request: RequestSchemaSpec
    response: ResponseSchemaSpec


@dataclass
class ResourceSchemaSpec:
    GET: Optional[SchemaSpec] = None
    HEAD: Optional[SchemaSpec] = None
    POST: Optional[SchemaSpec] = None
    PUT: Optional[SchemaSpec] = None
    DELETE: Optional[SchemaSpec] = None
    OPTIONS: Optional[SchemaSpec] = None
    TRACE: Optional[SchemaSpec] = None
    PATCH: Optional[SchemaSpec] = None
    CONNECT: Optional[SchemaSpec] = None


class SustainerdsResource:

    schema_spec: ResourceSchemaSpec = ResourceSchemaSpec()

    def __init__(self, app: falcon.API):
        pass




def validate_request(req: falcon.Request, spec: RequestSchemaSpec):
    '''Validates a request schema specification against the falcon.Request'''
    if spec.query:
        s = spec.query()
        s.load(req.params)

    if spec.json:
        s = spec.json()
        s.load(req.media)

    if spec.cookies:
        s = spec.cookies()
        s.load(req.cookies)

    if spec.headers:
        s = spec.headers()
        s.load(req.headers)


def validate_response(resp: falcon.Response, spec: ResponseSchemaSpec):
    '''Validates a response schema specification against the falcon.Response'''
    if spec.json:
        s = spec.json()
        s.load(resp.media)

    if spec.headers:
        s = spec.headers()
        s.load(resp.headers)

    
def validate_schema():
    def wrap(fn):
        def wrapped_f(cls, req: falcon.Request, resp: falcon.Response, *args):
            if cls.schema_spec:
                spec = getattr(cls.schema_spec, req.method)
                if not spec:
                    return fn(cls, req, resp, *args)

                if spec.request:
                    validate_request(req, spec.request)

                res = fn(cls, req, resp, *args)

                if spec.response:
                    validate_response(resp, spec.response)

                return res

        return wrapped_f
    return wrap
