import falcon
from typing import Callable, Dict, List, Optional
from types import ModuleType
from sustainerds.api.core.resource import SustainerdResource
from dataclasses import dataclass

@dataclass
class SustainerdsRoute:
    ''' Represents a route which we can define and return in our resources '''
    path: str
    resource: SustainerdResource
    kwargs: Dict

def add_routes(app: falcon.API, mod: ModuleType, fname: Optional[str] = None):
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
            app.add_route(r.path, r.resource, **r.kwargs)
    