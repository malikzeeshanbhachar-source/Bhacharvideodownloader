import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    """Test that the health endpoint returns a 200 OK response."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_response_structure() -> None:
    """Test that the health endpoint returns expected fields."""
    response = client.get("/health")
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"
    assert "service" in data
    assert "version" in data
