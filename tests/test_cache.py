import pytest
from unittest.mock import patch, MagicMock
from api.cache import get_cached, set_cached, invalidate

def test_get_cached_hit():
    """Cache hit — la clé existe"""
    mock_redis = MagicMock()
    mock_redis.get.return_value = '{"id": 1, "name": "Alice"}'

    with patch("api.cache.get_redis", return_value=mock_redis):
        result = get_cached("users:all")
        assert result == {"id": 1, "name": "Alice"}
        mock_redis.get.assert_called_once_with("users:all")

def test_get_cached_miss():
    """Cache miss — la clé n'existe pas"""
    mock_redis = MagicMock()
    mock_redis.get.return_value = None

    with patch("api.cache.get_redis", return_value=mock_redis):
        result = get_cached("users:all")
        assert result is None

def test_set_cached():
    """Stockage d'une valeur en cache avec TTL"""
    mock_redis = MagicMock()

    with patch("api.cache.get_redis", return_value=mock_redis):
        set_cached("users:all", [{"id": 1}], ttl=30)
        mock_redis.setex.assert_called_once()
        args = mock_redis.setex.call_args[0]
        assert args[0] == "users:all"
        assert args[1] == 30

def test_invalidate():
    """Suppression d'une clé du cache"""
    mock_redis = MagicMock()

    with patch("api.cache.get_redis", return_value=mock_redis):
        invalidate("users:all")
        mock_redis.delete.assert_called_once_with("users:all")