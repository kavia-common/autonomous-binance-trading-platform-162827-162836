from fastapi.testclient import TestClient

from src.domain.enums import TradingMode, OrderSide, OrderType


def test_health_root(client: TestClient):
    # App-level health at "/"
    r = client.get("/")
    assert r.status_code == 200
    data = r.json()
    # main.py root returns {"message": "Healthy"}
    assert "message" in data


def test_health_router(client: TestClient):
    # router health endpoint configured in routes/health.py also at "/"
    # Depending on include order, one of them responds; we assert OK either way
    r = client.get("/")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)


def test_signup_flow(client: TestClient):
    payload = {"email": "newuser@example.com", "password": "StrongPass!234", "full_name": "New User"}
    r = client.post("/auth/signup", json=payload)
    assert r.status_code == 200
    data = r.json()
    # AuthService.signup returns a User model with placeholder id
    assert data["email"] == payload["email"]
    assert "id" in data
    assert data["is_active"] is True


def test_login_placeholder(client: TestClient):
    # /auth/login expects form-encoded OAuth2PasswordRequestForm by default
    form = {"username": "testuser@example.com", "password": "irrelevant"}
    r = client.post("/auth/login", data=form)
    assert r.status_code == 200
    token = r.json()
    assert "access_token" in token
    assert token.get("token_type") == "bearer"


def test_me_protected(client: TestClient, auth_header):
    r = client.get("/auth/me", headers=auth_header)
    assert r.status_code == 200
    profile = r.json()
    assert "id" in profile
    # AuthService.me returns placeholder email, but id equals our JWT subject
    assert "email" in profile
    assert profile["is_active"] is True


def test_strategies_seed_and_upsert(client: TestClient, auth_header):
    # First list call seeds a default strategy if empty
    r = client.get("/strategies/", headers=auth_header)
    assert r.status_code == 200
    items = r.json()
    assert isinstance(items, list)
    assert len(items) >= 1
    first = items[0]
    assert "id" in first and "name" in first and "enabled" in first

    # Upsert a custom strategy
    upsert_payload = {"name": "My Breakout", "parameters": {"lookback": 20, "mult": 2.5}, "enabled": True}
    r2 = client.post("/strategies/", headers=auth_header, json=upsert_payload)
    assert r2.status_code == 200
    new_cfg = r2.json()
    assert new_cfg["name"] == "My Breakout"
    assert new_cfg["enabled"] is True
    assert "id" in new_cfg
    assert isinstance(new_cfg.get("parameters"), dict)

    # List again and ensure our upserted item is present among user strategies
    r3 = client.get("/strategies/", headers=auth_header)
    assert r3.status_code == 200
    names = [x["name"] for x in r3.json()]
    assert "My Breakout" in names


def test_trading_mode_switch_and_persist(client: TestClient, auth_header):
    # Switch to LIVE
    r = client.post("/trading/mode", headers=auth_header, json={"mode": "LIVE"})
    assert r.status_code == 200
    assert r.json() == "LIVE"

    # Switch back to DEMO
    r2 = client.post("/trading/mode", headers=auth_header, json={"mode": "DEMO"})
    assert r2.status_code == 200
    assert r2.json() == "DEMO"


def test_place_order_and_list_trades(client: TestClient, auth_header):
    # Ensure mode is DEMO initially (from earlier test may already be DEMO)
    client.post("/trading/mode", headers=auth_header, json={"mode": "DEMO"})

    # Place a demo MARKET BUY order
    payload = {"symbol": "BTCUSDT", "side": OrderSide.BUY.value, "type": OrderType.MARKET.value, "quantity": 0.01}
    r = client.post("/trading/order", headers=auth_header, json=payload)
    assert r.status_code == 200
    trade = r.json()
    assert trade["symbol"] == "BTCUSDT"
    assert trade["side"] == "BUY"
    assert trade["type"] == "MARKET"
    assert float(trade["quantity"]) == 0.01
    # Demo client returns a pseudo price
    assert trade.get("price") is not None
    # Mode should reflect current user mode
    assert trade.get("mode") == TradingMode.DEMO.value

    # List trades and ensure our trade is returned
    r2 = client.get("/trading/trades", headers=auth_header)
    assert r2.status_code == 200
    items = r2.json()
    assert isinstance(items, list)
    assert any(t["id"] == trade["id"] for t in items)


def test_analytics_snapshot_and_ws_info(client: TestClient, auth_header):
    # Snapshot should return a metrics array with at least one item and contain required fields
    r = client.get("/analytics/snapshot", headers=auth_header)
    # This route does not require auth in code, but we provide header consistently
    assert r.status_code == 200
    snap = r.json()
    assert "user_id" in snap
    assert "metrics" in snap
    assert isinstance(snap["metrics"], list)
    if snap["metrics"]:
        pt = snap["metrics"][0]
        # timestamp can be ISO string
        assert "equity" in pt and "pnl" in pt and "drawdown" in pt

    # WS info
    r2 = client.get("/analytics/websocket-info", headers=auth_header)
    assert r2.status_code == 200
    info = r2.json()
    assert info.get("endpoint") == "/ws/analytics"
    assert "protocol" in info
