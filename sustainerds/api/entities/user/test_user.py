def test_get_message(test_client):
    doc = {"email": "tim@elbart.com", "password": "bla123"}

    result = test_client.simulate_get("/user")
    assert result.json == doc
