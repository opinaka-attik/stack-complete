import pytest
from unittest.mock import patch, MagicMock

def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    data = r.get_json()
    assert data["status"]      == "ok"
    assert "environment" in data
    assert "version"     in data

def test_ready_tous_services_ok(client):
    mock_conn  = MagicMock()
    mock_redis = MagicMock()
    mock_redis.ping.return_value = True

    # ✅ Patcher au niveau module — là où health.py les importe
    with patch("api.routes.health.get_connection", return_value=mock_conn), \
         patch("api.routes.health.get_redis",      return_value=mock_redis):
        r = client.get("/ready")
        assert r.status_code == 200
        data = r.get_json()
        assert data["status"]             == "ready"
        assert data["checks"]["postgres"] == "ok"
        assert data["checks"]["redis"]    == "ok"

def test_ready_postgres_ko(client):
    mock_redis = MagicMock()
    mock_redis.ping.return_value = True

    with patch("api.routes.health.get_connection", side_effect=Exception("connexion refusée")), \
         patch("api.routes.health.get_redis",      return_value=mock_redis):
        r = client.get("/ready")
        assert r.status_code == 503
        data = r.get_json()
        assert data["status"]             == "degraded"
        assert "error" in data["checks"]["postgres"]

def test_ready_redis_ko(client):
    mock_conn  = MagicMock()
    mock_redis = MagicMock()
    mock_redis.ping.side_effect = Exception("redis indisponible")

    with patch("api.routes.health.get_connection", return_value=mock_conn), \
         patch("api.routes.health.get_redis",      return_value=mock_redis):
        r = client.get("/ready")
        assert r.status_code == 503
        data = r.get_json()
        assert data["status"]          == "degraded"
        assert "error" in data["checks"]["redis"]