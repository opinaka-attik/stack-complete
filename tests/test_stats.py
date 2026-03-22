from unittest.mock import patch, MagicMock

def test_stats(client):
    mock_redis = MagicMock()
    mock_redis.info.return_value = {
        "connected_clients" : 1,
        "used_memory_human" : "1.04M",
        "keyspace_hits"     : 10,
        "keyspace_misses"   : 2
    }

    with patch("api.cache.get_redis", return_value=mock_redis):
        r = client.get("/stats")
        assert r.status_code == 200
        data = r.get_json()
        assert "cache"                       in data
        assert data["cache"]["keyspace_hits"] == 10