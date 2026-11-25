
from is1.extensions import db
from is1.models import Categoria, Pregunta, Respuesta, RolUsuario, Usuario, Voto


def preparar_datos():
    usuario = Usuario(
        email="votos@test.com",
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

    respuesta = Respuesta(
        cuerpo="Respuesta de prueba",
        fechaPubli="2026-11-24T21:00:00",
        aceptada=False,
        pregunta_id=pregunta.id,
        autor_id=usuario.id,
        autor_tipo="USUARIO",
    )
    db.session.add(respuesta)
    db.session.commit()

    return usuario, pregunta, respuesta


def test_votar_positivamente_una_pregunta(client):
    usuario, pregunta, _ = preparar_datos()

    resultado = client.post(
        f"/preguntas/{pregunta.id}/votos",
        json={"usuario_id": usuario.id, "tipo": "POSITIVO"},
    )

    assert resultado.status_code == 201
    assert resultado.json["voto"]["tipo"] == "POSITIVO"


def test_cambiar_voto_de_una_pregunta(client):
    usuario, pregunta, _ = preparar_datos()

    client.post(
        f"/preguntas/{pregunta.id}/votos",
        json={"usuario_id": usuario.id, "tipo": "POSITIVO"},
    )

    resultado = client.post(
        f"/preguntas/{pregunta.id}/votos",
        json={"usuario_id": usuario.id, "tipo": "NEGATIVO"},
    )

    assert resultado.status_code == 200
    assert resultado.json["voto"]["tipo"] == "NEGATIVO"
    assert Voto.query.count() == 1


def test_votar_una_respuesta(client):
    usuario, _, respuesta = preparar_datos()

    resultado = client.post(
        f"/respuestas/{respuesta.id}/votos",
        json={"usuario_id": usuario.id, "tipo": "POSITIVO"},
    )

    assert resultado.status_code == 201
    assert resultado.json["voto"]["tipo"] == "POSITIVO"


def test_no_permitir_tipo_de_voto_invalido(client):
    usuario, pregunta, _ = preparar_datos()

    resultado = client.post(
        f"/preguntas/{pregunta.id}/votos",
        json={"usuario_id": usuario.id, "tipo": "NEUTRO"},
    )

    assert resultado.status_code == 400


def test_no_permitir_usuario_inexistente(client):
    _, pregunta, _ = preparar_datos()

    resultado = client.post(
        f"/preguntas/{pregunta.id}/votos",
        json={"usuario_id": 999, "tipo": "POSITIVO"},
    )

    assert resultado.status_code == 404
