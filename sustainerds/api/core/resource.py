from dataclasses import dataclass
from typing import Dict, List, Optional, Text, Tuple, Type

import falcon
import ujson
from marshmallow.exceptions import ValidationError
from marshmallow.schema import Schema

from sustainerds.api.core.persistence import PersistenceApi


HTTP_2xx = [
    falcon.HTTP_200,
    falcon.HTTP_201,
    falcon.HTTP_202,
    falcon.HTTP_203,
    falcon.HTTP_204,
    falcon.HTTP_205,
    falcon.HTTP_206,
    falcon.HTTP_207,
    falcon.HTTP_208,
]


@dataclass
class ResourceContext:
    """The context object containing configured persistence, auth, etc."""

    persistence: PersistenceApi


@dataclass
class RequestSchemaSpec:
    """Schema definition wrapper to cover all different locations to check for input data on the request"""

    query: Optional[Type[Schema]] = None
    json: Optional[Type[Schema]] = None
    headers: Optional[Type[Schema]] = None
    cookies: Optional[Type[Schema]] = None
    form: Optional[Type[Schema]] = None

    def __post_init__(self):
        if hasattr(self, "Query"):
            self.query = getattr(self, "Query")

        if hasattr(self, "Json"):
            self.json = getattr(self, "Json")

        if hasattr(self, "Headers"):
            self.headers = getattr(self, "Headers")

        if hasattr(self, "Cookies"):
            self.cookies = getattr(self, "Cookies")

        if hasattr(self, "Form"):
            self.form = getattr(self, "Form")


@dataclass
class ResponseSchemaSpec:
    """Schema definition wrapper to cover all different locations to check for output data on the response"""

    json: Optional[Type[Schema]] = None
    headers: Optional[Type[Schema]] = None

    def __post_init__(self):
        if hasattr(self, "Json"):
            self.json = getattr(self, "Json")

        if hasattr(self, "Headers"):
            self.headers = getattr(self, "Headers")


@dataclass
class SchemaSpec:
    """Wraps RequestSchemaSpec and ResponseSchemaSpec"""

    request: RequestSchemaSpec
    response: ResponseSchemaSpec


@dataclass
class ResourceSchemaSpec:
    """Defines all schema specifications for all HTTP methods"""

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

    def get_methods(self) -> List[Tuple[str, SchemaSpec]]:
        """Returns all defined methods and it's respective configuration"""

        def is_valid_method(m):
            if self.__dict__[m] is None:
                return False

            return isinstance(self.__dict__[m], SchemaSpec)

        return [
            (m, self.__dict__[m])
            # pylint: disable=no-member
            for m in self.__dataclass_fields__  # type: ignore
            if is_valid_method(m)
        ]


class BaseResource:
    """Base resource, which is used in the Sustainerds application"""

    ctx: ResourceContext
    name: Text

    @property
    def resource_schema_spec(self) -> ResourceSchemaSpec:
        """Property function, which describes all Schemas to validate for
           each HTTP verb for requests and Responses"""
        return ResourceSchemaSpec(name=self.name)

    def __init__(self, ctx: ResourceContext, name: Text):
        """Constructor for the Sustainerds resource

        Arguments:
        app: the falcon application.
        name: the name of the resource, which is used especially in the OpenAPI specification.
        """
        self.ctx = ctx
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
                s: Schema = spec.query()
                s.load(req.params)

            if spec.json:
                s = spec.json()
                req.validated = s.load(req.media)

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


class SchemaValidatorComponent:
    """A falcon middleware, which is used to validate request and response on a resource"""

    def process_resource(
        self,
        req: falcon.Request,
        resp: falcon.Response,
        resource: BaseResource,
        params: Dict,
    ):
        try:
            resource._validate_request_schema(req, resp, params)
        except ValidationError as ex:
            raise falcon.errors.HTTPUnprocessableEntity(
                description=ujson.dumps(ex.messages)
            )

    def process_response(
        self,
        req: falcon.Request,
        resp: falcon.Response,
        resource: BaseResource,
        params: Dict,
    ):
        try:
            if resp.status in HTTP_2xx:
                resource._validate_response_schema(req, resp, params)
        except ValidationError as ex:
            raise falcon.errors.HTTPUnprocessableEntity(
                description=ujson.dumps(ex.messages)
            )
