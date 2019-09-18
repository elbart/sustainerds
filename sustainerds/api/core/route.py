import falcon
from typing import Callable, Dict, List, Optional, Type, Optional
from types import ModuleType
from sustainerds.api.core.resource import SustainerdsResource
from dataclasses import dataclass
from apispec import APISpec

@dataclass
class SustainerdsRoute:
    ''' Represents a route which we can define and return in our entities '''
    path: str
    resource: Type[SustainerdsResource]
    kwargs: Optional[Dict] = None

def add_routes(app: falcon.API, spec: APISpec, mod: ModuleType, fname: Optional[str] = None):
    '''
    Looks up the `include_routes` callable within the
    passed module and executes the callable. The result
    of the callable is exepected to be of type `List[SustainerdsRoute]`.
    The list is iterated and each individual resource is added to the falcon app.
    '''
    fn = getattr(mod, fname if fname else 'include_routes')
    if fn:
        for r in fn(app):
            if not isinstance(r, SustainerdsRoute):
                raise ValueError(f'Object {r} required to be of type SustainerdsRoute, but was {type(r)}. Imported from module {mod}')
            resource = r.resource(app)

            if not r.kwargs:
                r.kwargs = {}

            app.add_route(r.path, resource, **r.kwargs)
            spec.path(resource=resource)
    