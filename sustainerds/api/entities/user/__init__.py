from sustainerds.api.core.route import SustainerdsRoute
from sustainerds.api.entities.user.resources import UserCollectionResource, UserResource


def include_routes(app):
    return [
        SustainerdsRoute("/user", UserCollectionResource, "UserCollection"),
        SustainerdsRoute("/user/{user_id}", UserResource, "UserCollection"),
    ]
