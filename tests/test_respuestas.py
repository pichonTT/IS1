
from is1.extensions import db
from is1.models import Categoria, Pregunta, Respuesta, RolUsuario, Usuario


def preparar_datos():
    usuario = Usuario(
        email="respuestas@test.com",
        contrasena="clave123",
        rol=RolUsuario.GENERAL,
    )
    categoria = Categoria(nombre="Programacion")

    db.session.add_all([usuario, categoria])
    db.session.commit()

    pregunta = Pregunta(
        titulo="Pregunta de prueba",
        cuerpo="Contenido de prueba",
        fechaPubli="2026-11-24T21:00:00",
        usuario_id=usuario.id,
        categoria_id=categoria.id,
    )

    db.session.add(pregunta)
    db.session.commit()

    return usuario, pregunta


def test_crear_respuesta_correctamente(client):
    usuario, pregunta = preparar_datos()

    resultado = client.post(
        f"/preguntas/{pregunta.id}/respuestas",
        json={
            "cuerpo": "Esta es una respuesta",
            "fechaPubli": "2026-11-24",
            "autor_tipo": "USUARIO",
            "autor_id": usuario.id,
        },
    )

    assert resultado.status_code == 201
    assert resultado.json["autor_tipo"] == "USUARIO"


def test_no_crear_respuesta_sin_datos(client):
    _, pregunta = preparar_datos()

    resultado = client.post(
        f"/preguntas/{pregunta.id}/respuestas",
        json={},
    )

    assert resultado.status_code == 400


def test_no_crear_respuesta_para_pregunta_inexistente(client):
    usuario, _ = preparar_datos()

    resultado = client.post(
        "/preguntas/999/respuestas",
        json={
            "cuerpo": "Respuesta",
            "fechaPubli": "2026-11-24",
            "autor_tipo": "USUARIO",
            "autor_id": usuario.id,
        },
    )

    assert resultado.status_code == 404


def test_aceptar_respuesta_correctamente(client):
    usuario, pregunta = preparar_datos()

    respuesta = Respuesta(
        cuerpo="Respuesta de prueba",
        fechaPubli="2026-11-24",
        aceptada=False,
        pregunta_id=pregunta.id,
        autor_id=usuario.id,
        autor_tipo="USUARIO",
    )

    db.session.add(respuesta)
    db.session.commit()

    resultado = client.patch(
        f"/preguntas/{pregunta.id}/respuestas/{respuesta.id}/aceptar",
        json={"usuario_id": usuario.id},
    )

    assert resultado.status_code == 200
    assert resultado.json["aceptada"] is True


def test_otro_usuario_no_puede_aceptar_respuesta(client):
    _usuario, pregunta = preparar_datos()

    otro_usuario = Usuario(
        email="otro@test.com",
        contrasena="clave123",
        rol=RolUsuario.GENERAL,
    )
    db.session.add(otro_usuario)
    db.session.commit()

    respuesta = Respuesta(
        cuerpo="Respuesta de prueba",
        fechaPubli="2026-11-24",
        aceptada=False,
        pregunta_id=pregunta.id,
        autor_id=otro_usuario.id,
        autor_tipo="USUARIO",
    )

    db.session.add(respuesta)
    db.session.commit()

    resultado = client.patch(
        f"/preguntas/{pregunta.id}/respuestas/{respuesta.id}/aceptar",
        json={"usuario_id": otro_usuario.id},
    )

    assert resultado.status_code == 403
