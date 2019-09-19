from sustainerds.api.core.route import SustainerdsRoute
from sustainerds.api.entities.user.resources import UserCollectionResource


def include_routes(app):
    return [SustainerdsRoute("/user", UserCollectionResource, "UserCollection")]
