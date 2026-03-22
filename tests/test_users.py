def test_list_users_depuis_cache(client, mock_db, mock_cache):
    mock_get_cached, _, _ = mock_cache
    mock_get_cached.return_value = [
        {"id": 1, "name": "Alice", "email": "alice@test.com"}
    ]

    r = client.get("/users")
    assert r.status_code == 200
    data = r.get_json()
    assert data["source"] == "cache"          # vient du cache
    assert len(data["data"]) == 1

def test_list_users_depuis_bdd(client, mock_db, mock_cache):
    mock_get_cached, mock_set_cached, _ = mock_cache
    mock_get_users, _                   = mock_db

    mock_get_cached.return_value = None       # cache vide
    mock_get_users.return_value  = [
        {"id": 1, "name": "Bob", "email": "bob@test.com"}
    ]

    r = client.get("/users")
    assert r.status_code == 200
    data = r.get_json()
    assert data["source"] == "database"       # vient de la BDD

def test_create_user(client, mock_db, mock_cache):
    _, mock_create_user         = mock_db
    _, _, mock_invalidate       = mock_cache
    mock_create_user.return_value = {
        "id": 2, "name": "Carol", "email": "carol@test.com"
    }

    r = client.post("/users", json={
        "name" : "Carol",
        "email": "carol@test.com"
    })
    assert r.status_code == 201
    mock_invalidate.assert_called_once_with("users:all")  # cache invalidé

def test_create_user_champs_manquants(client):
    r = client.post("/users", json={"name": "Dave"})
    assert r.status_code == 400
    assert "error" in r.get_json()