import pytest
from app.main import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json["status"] == "healthy"

def test_orders(client):
    resp = client.get("/api/orders")
    assert resp.status_code == 200
    assert len(resp.json["orders"]) == 2
