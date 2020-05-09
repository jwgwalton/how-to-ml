from fastapi.testclient import TestClient

from app.server import app

client = TestClient(app)


def test_info_endpoint():
    response = client.get("/info")
    assert response.status_code == 200
    assert response.json() == {
        "description": "A microservice for predicting the species of iris",
        "version": "0.0.0",
        "model_name": "iris_classification_fdd13277-d1e8-4e26-a88d-b63e9596f766"
    }
