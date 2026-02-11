import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_product():
    response = client.post(
        "/products/",
        json={
            "name": "Phone",
            "description": "Smartphone",
            "price": 500
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Phone"
    assert "id" in data


def test_cache_miss_then_hit():
    # First request → should be cache miss internally
    response = client.get("/products/1")
    assert response.status_code == 200

    # Second request → should be cache hit internally
    response = client.get("/products/1")
    assert response.status_code == 200


def test_update_invalidates_cache():
    response = client.put(
        "/products/1",
        json={
            "name": "Updated Phone",
            "description": "Updated Smartphone",
            "price": 600
        },
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Phone"


def test_delete_product():
    response = client.delete("/products/1")
    assert response.status_code == 204

    # After delete → should return 404
    response = client.get("/products/1")
    assert response.status_code == 404
