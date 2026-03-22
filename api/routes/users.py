from flask import Blueprint, jsonify, request
from api.database import get_all_users, create_user
from api.cache    import get_cached, set_cached, invalidate

users_bp = Blueprint("users", __name__)

@users_bp.route("/users", methods=["GET"])
def list_users():
    # Vérifier le cache d'abord
    cached = get_cached("users:all")
    if cached:
        return jsonify({"source": "cache", "data": cached})

    # Sinon aller en base
    users = get_all_users()
    set_cached("users:all", users, ttl=30)
    return jsonify({"source": "database", "data": users})

@users_bp.route("/users", methods=["POST"])
def add_user():
    body  = request.get_json()
    name  = body.get("name")
    email = body.get("email")

    if not name or not email:
        return jsonify({"error": "name et email requis"}), 400

    user = create_user(name, email)
    invalidate("users:all")    # invalider le cache après écriture
    return jsonify(user), 201