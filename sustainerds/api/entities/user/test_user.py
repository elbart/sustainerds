from falcon import testing
import pytest

import sustainerds.api.app as sustainerds_app


# Depending on your testing strategy and how your application
# manages state, you may be able to broaden the fixture scope
# beyond the default 'function' scope used in this example.

@pytest.fixture()
def client():
    # Assume the hypothetical `myapp` package has a function called
    # `create()` to initialize and return a `falcon.API` instance.
    return testing.TestClient(sustainerds_app.create())


def test_get_message(client):
    doc = {
            "email": "tim@elbart.com",
            "password": "bla123",
        }

    result = client.simulate_get('/user')
    assert result.json == doc
