
import os


class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "clave-desarrollo-is1-cambiar-en-produccion",
    )

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///is1.db",
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
