from flask import Flask
import os

def create_app():
    app = Flask(__name__)

    # Enregistrer les blueprints
    from api.routes.health import health_bp
    from api.routes.users  import users_bp
    from api.routes.stats  import stats_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(stats_bp)

    return app

app = create_app()

if __name__ == "__main__":
    from api.database import init_db
    init_db()                              # créer les tables au démarrage
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)