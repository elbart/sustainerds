from falcon.testing import Result, TestClient

from sustainerds.api.entities.user.model import UserDbModel


###############################################################################
# model tests
###############################################################################
def test_something():
    d = UserDbModel()
    d.email = "tim@elbart.com"
    d.password = "secret123"


###############################################################################
# endpoint tests
###############################################################################
def test_register_user(test_client: TestClient):
    doc = {"email": "tim@elbart.com", "password": "bla123"}
    result: Result = test_client.simulate_post("/user", json=doc)

    assert result.status_code == 200
    data = result.json

    result2: Result = test_client.simulate_get(f"/user/{data['id']}")
    assert result2.status_code == 200

    assert data == result2.json
