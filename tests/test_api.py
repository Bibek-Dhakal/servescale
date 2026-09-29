import os

import pytest
from fastapi.testclient import TestClient

# Mock settings before importing app
os.environ["ENVIRONMENT"] = "testing"

from app.config import settings  # noqa: E402
from app.main import app  # noqa: E402

# Standard synchronous TestClient
client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_predict_endpoint_valid_input():
    # Only test inference if model is generated
    if not os.path.exists(settings.model_path):
        pytest.skip(f"Model not found at {settings.model_path}. Run generate_model.py first.")

    payload = {"features": [[0.1] * 10, [0.9] * 10]}

    # We must invoke lifespan events for TestClient in FastAPI to trigger the ML loader
    with TestClient(app) as live_client:
        response = live_client.post("/predict", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert "predictions" in data
        assert len(data["predictions"]) == 2


def test_predict_endpoint_invalid_input():
    # Only test inference if model is generated
    if not os.path.exists(settings.model_path):
        pytest.skip(f"Model not found at {settings.model_path}. Run generate_model.py first.")

    payload = {"features": "not-a-list"}

    with TestClient(app) as live_client:
        response = live_client.post("/predict", json=payload)
        assert response.status_code == 422  # Validation error
