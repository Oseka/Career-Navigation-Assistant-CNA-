def test_health_returns_ok(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_unknown_api_path_returns_error_envelope(client):
    response = client.get("/api/does-not-exist")
    body = response.get_json()

    assert response.status_code == 404
    assert body["error"]["code"] == "NOT_FOUND"
    assert body["error"]["message"]
