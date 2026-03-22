import os
import redis
import json
from datetime import datetime, date

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# ✅ Encodeur personnalisé pour les types non sérialisables
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()    # "2026-03-22T17:28:48"
        return super().default(obj)

def get_redis():
    return redis.from_url(REDIS_URL, decode_responses=True)

def get_cached(key):
    r   = get_redis()
    val = r.get(key)
    return json.loads(val) if val else None

def set_cached(key, value, ttl=60):
    r = get_redis()
    # ✅ Utiliser le CustomEncoder
    r.setex(key, ttl, json.dumps(value, cls=CustomEncoder))

def invalidate(key):
    r = get_redis()
    r.delete(key)

def get_stats():
    r    = get_redis()
    info = r.info()
    return {
        "connected_clients" : info["connected_clients"],
        "used_memory_human" : info["used_memory_human"],
        "keyspace_hits"     : info.get("keyspace_hits",   0),
        "keyspace_misses"   : info.get("keyspace_misses", 0)
    }