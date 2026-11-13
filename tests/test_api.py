def test_health_route():
    from fastapi.testclient import TestClient
    from api.routes import app
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
