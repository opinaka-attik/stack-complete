from flask import Blueprint, jsonify
from api.cache import get_stats

stats_bp = Blueprint("stats", __name__)

@stats_bp.route("/stats")
def stats():
    return jsonify({
        "cache" : get_stats()
    })