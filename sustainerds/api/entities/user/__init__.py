from sustainerds.api.core.routes import SustainerdsRoute
from sustainerds.api.entities.user.resources import S12nUserResource
def include_routes(app):
    return [
        SustainerdsRoute("/user", S12nUserResource(), {})
    ]
