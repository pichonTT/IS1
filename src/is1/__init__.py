
from flask import Flask

from is1.api.health import health_bp
from is1.extensions import db
from is1.config import Config


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(health_bp)

    return app
