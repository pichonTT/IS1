
from flask import Flask

from is1.api.health import health_bp
from is1.api.preguntas import preguntas_bp
from is1.api.respuestas import respuestas_bp
from is1.api.usuarios import usuarios_bp
from is1.api.votos import votos_bp
from is1.config import Config
from is1.extensions import db, migrate
from is1.services.programador_ia import iniciar_programador
from is1.web import web_bp


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(health_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(preguntas_bp)
    app.register_blueprint(respuestas_bp)
    app.register_blueprint(votos_bp)
    app.register_blueprint(web_bp)

    iniciar_programador(app)

    return app
