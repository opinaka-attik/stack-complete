def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    data = r.get_json()
    assert data["status"] == "ok"
    assert "environment" in data
    assert "version"     in data

def test_ready_avec_services_ok(client):
    from unittest.mock import patch, MagicMock

    mock_conn  = MagicMock()
    mock_redis = MagicMock()
    mock_redis.ping.return_value = True

    with patch("api.routes.health.get_connection", return_value=mock_conn), \
         patch("api.routes.health.get_redis",      return_value=mock_redis):
        r = client.get("/ready")
        assert r.status_code == 200
        data = r.get_json()
        assert data["status"]           == "ready"
        assert data["checks"]["postgres"] == "ok"
        assert data["checks"]["redis"]    == "ok"