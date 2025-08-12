from fastapi.testclient import TestClient
from uuid import uuid4
from main import app, Product

client = TestClient(app)

def test_create_product():
    product_data = {
        "id": str(uuid4()),
        "name": "Test Product",
        "description": "A product for testing",
        "price": 99.99
    }
    response = client.post("/products/", json=product_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["price"] == product_data["price"]

def test_list_products():
    response = client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_product():
    # First create a product
    product_data = {
        "id": str(uuid4()),
        "name": "Another Product",
        "description": "Another description",
        "price": 50.0
    }
    client.post("/products/", json=product_data)
    response = client.get(f"/products/{product_data['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_data["id"]

def test_update_product():
    product_data = {
        "id": str(uuid4()),
        "name": "Product to update",
        "description": "Old description",
        "price": 20.0
    }
    client.post("/products/", json=product_data)
    updated_data = product_data.copy()
    updated_data["name"] = "Updated Product"
    updated_data["price"] = 25.0

    response = client.put(f"/products/{product_data['id']}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Product"
    assert data["price"] == 25.0

def test_delete_product():
    product_data = {
        "id": str(uuid4()),
        "name": "Product to delete",
        "description": "To be deleted",
        "price": 10.0
    }
    client.post("/products/", json=product_data)
    response = client.delete(f"/products/{product_data['id']}")
    assert response.status_code == 204

    # Confirm deletion
    response = client.get(f"/products/{product_data['id']}")
    assert response.status_code == 404
