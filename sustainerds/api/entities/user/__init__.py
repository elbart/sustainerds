from sustainerds.api.core.route import SustainerdsRoute
from sustainerds.api.entities.user.resources import UserResource

def include_routes(app):
    return [
        SustainerdsRoute("/user", UserResource)
    ]
