from flask import Blueprint, jsonify
import os

health_bp = Blueprint("health", __name__)

@health_bp.route("/health")
def health():
    return jsonify({
        "status"      : "ok",
        "environment" : os.getenv("APP_ENV", "local"),
        "version"     : os.getenv("APP_VERSION", "1.0.0")
    })

@health_bp.route("/ready")
def ready():
    """Vérifie que tous les services sont disponibles"""
    from api.database import get_connection
    from api.cache    import get_redis
    checks = {}

    # Vérif PostgreSQL
    try:
        conn = get_connection()
        conn.close()
        checks["postgres"] = "ok"
    except Exception as e:
        checks["postgres"] = f"error: {str(e)}"

    # Vérif Redis
    try:
        r = get_redis()
        r.ping()
        checks["redis"] = "ok"
    except Exception as e:
        checks["redis"] = f"error: {str(e)}"

    all_ok = all(v == "ok" for v in checks.values())
    return jsonify({
        "status" : "ready" if all_ok else "degraded",
        "checks" : checks
    }), 200 if all_ok else 503