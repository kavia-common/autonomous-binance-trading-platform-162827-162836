from fastapi.testclient import TestClient


def test_protected_routes_require_auth(client: TestClient):
    # /auth/me requires Authorization
    r = client.get("/auth/me")
    assert r.status_code == 401

    # Trading endpoints require Authorization
    r2 = client.get("/trading/trades")
    assert r2.status_code == 401

    r3 = client.post("/trading/order", json={"symbol": "BTCUSDT", "side": "BUY", "type": "MARKET", "quantity": 0.01})
    assert r3.status_code == 401

    r4 = client.post("/trading/mode", json={"mode": "DEMO"})
    assert r4.status_code == 401
