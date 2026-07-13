from fastapi.testclient import TestClient

from app.main import app


def test_root_returns_ok():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_build_endpoint_index():
    specification = {
        "openapi": "3.0.3",
        "paths": {
            "/customers": {
                "post": {
                    "operationId": "createCustomer",
                    "summary": "Create a customer",
                    "responses": {"201": {"description": "Created"}},
                }
            }
        },
    }
