from flask import Flask, jsonify

from config import Config
from extensions import db, migrate, bcrypt, jwt
from models import User, Note
from controllers.auth import auth_bp
from controllers.notes import notes_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)

    @app.route("/")
    def home():
        return jsonify({
            "message": "Personal Productivity API is running"
        }), 200

    @app.route("/api/health")
    def health():
        return jsonify({
            "status": "ok",
            "message": "API is healthy"
        }), 200

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
