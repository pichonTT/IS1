
from datetime import datetime

from flask import Blueprint, jsonify, request

from is1.extensions import db
from is1.models import Pregunta, Respuesta, Tipo_Voto, Usuario, Voto

votos_bp = Blueprint("votos", __name__)


def registrar_voto(elemento, campo):
    datos = request.get_json(silent=True) or {}

    usuario_id = datos.get("usuario_id")
    tipo = datos.get("tipo")

    if usuario_id is None or tipo is None:
        return jsonify({"error": "Faltan usuario_id o tipo"}), 400

    usuario = db.session.get(Usuario, usuario_id)

    if usuario is None:
        return jsonify({"error": "El usuario no existe"}), 404

    try:
        tipo_voto = Tipo_Voto(tipo.upper())
    except (ValueError, AttributeError):
        return jsonify({
            "error": "El tipo debe ser POSITIVO o NEGATIVO"
        }), 400

    filtro = {
        "usuario_id": usuario_id,
        campo: elemento.id,
    }

    voto = Voto.query.filter_by(**filtro).first()

    if voto is None:
        voto = Voto(
            usuario_id=usuario_id,
            tipo=tipo_voto,
            fecha=datetime.now().isoformat(timespec="seconds"),
            pregunta_id=elemento.id if campo == "pregunta_id" else None,
            respuesta_id=elemento.id if campo == "respuesta_id" else None,
        )
        db.session.add(voto)
        estado = 201
        mensaje = "Voto registrado"
    else:
        voto.tipo = tipo_voto
        voto.fecha = datetime.now().isoformat(timespec="seconds")
        estado = 200
        mensaje = "Voto actualizado"

    db.session.commit()

    return jsonify({
        "mensaje": mensaje,
        "voto": {
            "id": voto.id,
            "tipo": voto.tipo.value,
            "usuario_id": voto.usuario_id,
            "pregunta_id": voto.pregunta_id,
            "respuesta_id": voto.respuesta_id,
            "fecha": voto.fecha,
        },
    }), estado


@votos_bp.route(
    "/preguntas/<int:pregunta_id>/votos",
    methods=["POST"]
)
def votar_pregunta(pregunta_id):
    pregunta = db.session.get(Pregunta, pregunta_id)

    if pregunta is None:
        return jsonify({"error": "La pregunta no existe"}), 404

    return registrar_voto(pregunta, "pregunta_id")


@votos_bp.route(
    "/respuestas/<int:respuesta_id>/votos",
    methods=["POST"]
)
def votar_respuesta(respuesta_id):
    respuesta = db.session.get(Respuesta, respuesta_id)

    if respuesta is None:
        return jsonify({"error": "La respuesta no existe"}), 404

    return registrar_voto(respuesta, "respuesta_id")
