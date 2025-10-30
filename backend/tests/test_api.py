import os
os.environ["JWT_SECRET"] = "testsecret"
os.environ["DATABASE_URL"] = "sqlite:///./test.db"


from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def auth_header():
    r = client.post("/auth/login", json={"username":"admin","password":"password"})
    assert r.status_code == 200
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_and_filter_estimates():
    # Create
    payload = {
    "customer_name": "Charlie",
    "vehicle": "Ford Fiesta 2016",
    "description": "Oil change",
    "amount": 59.99
    }
    r = client.post("/estimates", json=payload, headers=auth_header())
    assert r.status_code == 201
    eid = r.json()["id"]


    # List all
    r = client.get("/estimates", headers=auth_header())
    assert r.status_code == 200
    assert any(e["id"] == eid for e in r.json())


    # Update status
    r = client.patch(f"/estimates/{eid}/status", json={"status":"APPROVED"}, headers=auth_header())
    assert r.status_code == 200
    assert r.json()["status"] == "APPROVED"


    # Filter by status
    r = client.get("/estimates", params={"status":"APPROVED"}, headers=auth_header())
    assert r.status_code == 200
    assert all(e["status"] == "APPROVED" for e in r.json())