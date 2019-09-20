from falcon.testing import Result, TestClient


###############################################################################
# model tests
###############################################################################

###############################################################################
# endpoint tests
###############################################################################
def test_get_message(test_client: TestClient):
    doc = {"email": "tim@elbart.com", "password": "bla123"}

    result: Result = test_client.simulate_get("/user")
    assert result.json == doc
