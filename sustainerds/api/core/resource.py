from dataclasses import dataclass
from typing import Dict, Optional, Text, Type

import falcon
from marshmallow.schema import Schema


@dataclass
class RequestSchemaSpec:
    """Schema definition wrapper to cover all different locations to check for input data on the request"""

    query: Optional[Type[Schema]] = None
    json: Optional[Type[Schema]] = None
    headers: Optional[Type[Schema]] = None
    cookies: Optional[Type[Schema]] = None
    form: Optional[Type[Schema]] = None


@dataclass
class ResponseSchemaSpec:
    """Schema definition wrapper to cover all different locations to check for output data on the response"""

    json: Optional[Type[Schema]] = None
    headers: Optional[Type[Schema]] = None


@dataclass
class SchemaSpec:
    request: RequestSchemaSpec
    response: ResponseSchemaSpec


@dataclass
class ResourceSchemaSpec:
    name: Text
    GET: Optional[SchemaSpec] = None
    HEAD: Optional[SchemaSpec] = None
    POST: Optional[SchemaSpec] = None
    PUT: Optional[SchemaSpec] = None
    DELETE: Optional[SchemaSpec] = None
    OPTIONS: Optional[SchemaSpec] = None
    TRACE: Optional[SchemaSpec] = None
    PATCH: Optional[SchemaSpec] = None
    CONNECT: Optional[SchemaSpec] = None

    def get_operations(self):
        def is_valid_operation(op):
            if self.__dict__[op] is None:
                return False

            return isinstance(self.__dict__[op], SchemaSpec)

        return [
            (op, self.__dict__[op])
            # pylint: disable=no-member
            for op in self.__dataclass_fields__
            if is_valid_operation(op)
        ]


class SustainerdsResource:
    @property
    def resource_schema_spec(self) -> ResourceSchemaSpec:
        return ResourceSchemaSpec(name=self.name)

    def __init__(self, app: falcon.API, name):
        self.app = app
        self.name = name

    def _validate_request_schema(
        self, req: falcon.Request, resp: falcon.Response, params: Dict
    ):
        """Validates a request schema specification against the falcon.Request"""
        if self.resource_schema_spec:
            schema_spec: SchemaSpec = getattr(self.resource_schema_spec, req.method)
            if not schema_spec or not schema_spec.request:
                return

            spec: RequestSchemaSpec = schema_spec.request

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

    def _validate_response_schema(
        self, req: falcon.Request, resp: falcon.Response, params: Dict
    ):
        """Validates a response schema specification against the falcon.Response"""
        if self.resource_schema_spec:
            schema_spec: SchemaSpec = getattr(self.resource_schema_spec, req.method)
            if not schema_spec or not schema_spec.response:
                return

            spec: ResponseSchemaSpec = schema_spec.response

            if spec.json:
                s = spec.json()
                s.load(resp.media)

            if spec.headers:
                s = spec.headers()
                s.load(resp.headers)


def validate_request(req: falcon.Request, spec: RequestSchemaSpec):
    """Validates a request schema specification against the falcon.Request"""
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
    """Validates a response schema specification against the falcon.Response"""
    if spec.json:
        s = spec.json()
        s.load(resp.media)

    if spec.headers:
        s = spec.headers()
        s.load(resp.headers)


class SchemaValidatorComponent:
    """A falcon middleware, which is used to validate request and response on a resource"""

    def process_resource(
        self,
        req: falcon.Request,
        resp: falcon.Response,
        resource: SustainerdsResource,
        params: Dict,
    ):
        resource._validate_request_schema(req, resp, params)

    def process_response(
        self,
        req: falcon.Request,
        resp: falcon.Response,
        resource: SustainerdsResource,
        params: Dict,
    ):
        resource._validate_response_schema(req, resp, params)
