import pytest
from unittest.mock import patch, MagicMock
from api.app import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def mock_db():
    """Mock PostgreSQL — pas besoin de vraie BDD pour les tests unitaires"""
    with patch("api.routes.users.get_all_users") as mock_get, \
         patch("api.routes.users.create_user")   as mock_create:
        yield mock_get, mock_create

@pytest.fixture
def mock_cache():
    """Mock Redis — pas besoin de vrai Redis pour les tests unitaires"""
    with patch("api.routes.users.get_cached")  as mock_get, \
         patch("api.routes.users.set_cached")  as mock_set, \
         patch("api.routes.users.invalidate")  as mock_inv:
        yield mock_get, mock_set, mock_inv