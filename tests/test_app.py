from api.app import create_app

def test_create_app():
    """L'app se crée sans erreur"""
    app = create_app()
    assert app is not None

def test_blueprints_enregistres():
    """Tous les blueprints sont bien enregistrés"""
    app   = create_app()
    rules = [str(r) for r in app.url_map.iter_rules()]
    assert "/health" in rules
    assert "/ready"  in rules
    assert "/users"  in rules
    assert "/stats"  in rules