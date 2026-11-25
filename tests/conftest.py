
import pytest
from flask import Flask

from is1.api.respuestas import respuestas_bp
from is1.api.usuarios import usuarios_bp
from is1.api.votos import votos_bp
from is1.extensions import db


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(votos_bp)
    app.register_blueprint(respuestas_bp)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
