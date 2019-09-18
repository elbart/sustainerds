from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
import falcon
from falcon_apispec import FalconPlugin
from marshmallow import Schema, fields
from sustainerds.api.core.route import add_routes
import sustainerds.api.entities.user as user


# Optional marshmallow support
class CategorySchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)

class PetSchema(Schema):
    category = fields.Nested(CategorySchema, many=True)
    name = fields.Str()


class RandomPetResource:
    def on_get(self, req, resp):
        """A cute furry animal endpoint.
        ---
        description: Get a random pet
        responses:
            200:
                description: A pet to be returned
                schema: PetSchema
        """
        pet = '{}'  # returns JSON
        resp.media = pet


def create(sqla_session=None):
    '''Creates the falcon app and takes the respective arguments we need:
    - database
    - filesystem
    - configuration
    - etc.
    '''
    # Create Falcon web app
    app = falcon.API()
    # create instance of resource
    random_pet_resource = RandomPetResource()
    # pass into `add_route` for Falcon
    app.add_route("/random", random_pet_resource)

    # Create an APISpec
    spec = APISpec(
        title='Swagger Petstore',
        version='1.0.0',
        openapi_version='2.0',
        plugins=[
            FalconPlugin(app),
            MarshmallowPlugin(),
        ],
    )

    add_routes(app, spec, user)

    # Register entities and paths
    spec.components.schema('Category', schema=CategorySchema)
    spec.components.schema('Pet', schema=PetSchema)
    return app


def get_app():
    '''The actual wsgi application factory which is stitching all the
    required things together'''
    return create()