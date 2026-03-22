import pytest
from unittest.mock import patch, MagicMock
from api.database import get_all_users, create_user, serialize_user
from datetime import datetime

def test_serialize_user():
    """Conversion datetime → string ISO"""
    user = {
        "id"        : 1,
        "name"      : "Alice",
        "email"     : "alice@test.com",
        "created_at": datetime(2026, 3, 22, 17, 28, 48)
    }
    result = serialize_user(user)
    assert result["created_at"] == "2026-03-22T17:28:48"

def test_serialize_user_sans_date():
    """Sérialisation sans champ created_at"""
    user   = {"id": 1, "name": "Bob", "email": "bob@test.com"}
    result = serialize_user(user)
    assert result == user

def test_get_all_users():
    """Récupération de tous les utilisateurs"""
    mock_conn = MagicMock()
    mock_cur  = MagicMock()
    mock_conn.cursor.return_value = mock_cur
    mock_cur.fetchall.return_value = [
        {"id": 1, "name": "Alice", "email": "alice@test.com",
         "created_at": datetime(2026, 3, 22)}
    ]

    with patch("api.database.get_connection", return_value=mock_conn):
        users = get_all_users()
        assert len(users) == 1
        assert users[0]["name"]       == "Alice"
        assert users[0]["created_at"] == "2026-03-22T00:00:00"

def test_create_user():
    """Création d'un utilisateur"""
    mock_conn = MagicMock()
    mock_cur  = MagicMock()
    mock_conn.cursor.return_value = mock_cur
    mock_cur.fetchone.return_value = {
        "id"        : 5,
        "name"      : "Carol",
        "email"     : "carol@test.com",
        "created_at": datetime(2026, 3, 22, 10, 0, 0)
    }

    with patch("api.database.get_connection", return_value=mock_conn):
        user = create_user("Carol", "carol@test.com")
        assert user["id"]    == 5
        assert user["name"]  == "Carol"
        assert user["email"] == "carol@test.com"
        mock_conn.commit.assert_called_once()