import os
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.getenv("DATABASE_URL",
    "postgresql://user:password@localhost:5432/appdb")

def get_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def init_db():
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id         SERIAL PRIMARY KEY,
            name       VARCHAR(100) NOT NULL,
            email      VARCHAR(100) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def serialize_user(user):
    """✅ Convertit un user dict en objet sérialisable JSON"""
    u = dict(user)
    if "created_at" in u and u["created_at"] is not None:
        u["created_at"] = u["created_at"].isoformat()
    return u

def get_all_users():
    conn  = get_connection()
    cur   = conn.cursor()
    cur.execute("SELECT * FROM users ORDER BY created_at DESC")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return [serialize_user(u) for u in users]    # ✅ sérialiser ici

def create_user(name, email):
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING *",
        (name, email)
    )
    user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return serialize_user(user)    # ✅ sérialiser ici