
from werkzeug.security import check_password_hash

from is1.extensions import db
from is1.models import RolUsuario, Usuario


def test_registrar_usuario_correctamente(client):
    respuesta = client.post(
        "/usuarios",
        json={
            "email": "usuario@test.com",
            "contrasena": "clave123",
        },
    )

    assert respuesta.status_code == 201
    assert respuesta.json["email"] == "usuario@test.com"
    assert respuesta.json["rol"] == "GENERAL"

    usuario = db.session.query(Usuario).first()

    assert usuario is not None
    assert usuario.rol == RolUsuario.GENERAL
    assert check_password_hash(usuario.contrasena, "clave123")


def test_registrar_usuario_sin_datos(client):
    respuesta = client.post("/usuarios", json={})

    assert respuesta.status_code == 400


def test_registrar_usuario_sin_email(client):
    respuesta = client.post(
        "/usuarios",
        json={"contrasena": "clave123"},
    )

    assert respuesta.status_code == 400


def test_registrar_usuario_sin_contrasena(client):
    respuesta = client.post(
        "/usuarios",
        json={"email": "usuario@test.com"},
    )

    assert respuesta.status_code == 400


def test_registrar_email_duplicado(client):
    datos = {
        "email": "usuario@test.com",
        "contrasena": "clave123",
    }

    primera = client.post("/usuarios", json=datos)
    segunda = client.post("/usuarios", json=datos)

    assert primera.status_code == 201
    assert segunda.status_code == 409
