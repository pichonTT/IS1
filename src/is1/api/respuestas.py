
from datetime import date

from flask import Blueprint, jsonify, request

from is1.extensions import db
from is1.models import AgenteIA, Pregunta, Respuesta, Usuario
from is1.services.automatizacion_ia import (
    procesar_preguntas_sin_respuesta,
)
from is1.services.estrategias.estrategia_gemini import EstrategiaGemini
from is1.services.estrategias.estrategia_modelo_local import (
    EstrategiaModeloLocal,
)
from is1.services.estrategias.estrategia_openai import EstrategiaOpenAI

respuestas_bp = Blueprint("respuestas", __name__)


@respuestas_bp.post("/preguntas/<int:pregunta_id>/respuestas")
def crear_respuesta(pregunta_id):
    datos = request.get_json()

    if not datos:
        return jsonify(error="Se requiere un JSON"), 400

    cuerpo = datos.get("cuerpo")
    fecha = datos.get("fechaPubli")
    autor_tipo = datos.get("autor_tipo")
    autor_id = datos.get("autor_id")

    if not cuerpo or not fecha or not autor_tipo or autor_id is None:
        return jsonify(error="Faltan datos obligatorios"), 400

    pregunta = db.session.get(Pregunta, pregunta_id)

    if pregunta is None:
        return jsonify(error="Pregunta inexistente"), 404

    if autor_tipo == "USUARIO":
        autor = db.session.get(Usuario, autor_id)
    elif autor_tipo == "AGENTE_IA":
        autor = db.session.get(AgenteIA, autor_id)
    else:
        return jsonify(error="Tipo de autor inválido"), 400

    if autor is None:
        return jsonify(error="Autor inexistente"), 404

    respuesta = Respuesta(
        cuerpo=cuerpo,
        fechaPubli=fecha,
        pregunta_id=pregunta.id
    )

    respuesta.establecerAutor(autor)
    db.session.add(respuesta)
    db.session.commit()

    return jsonify(
        mensaje="Respuesta creada correctamente",
        id=respuesta.id,
        pregunta_id=pregunta.id,
        autor_id=respuesta.autor_id,
        autor_tipo=respuesta.autor_tipo
    ), 201


@respuestas_bp.post("/preguntas/<int:pregunta_id>/respuestas/ia")
def generar_respuesta_ia(pregunta_id):
    datos = request.get_json()

    if not datos:
        return jsonify(error="Se requiere un JSON"), 400

    nombre_estrategia = datos.get("estrategia")

    estrategias = {
        "gemini": EstrategiaGemini,
        "openai": EstrategiaOpenAI,
        "local": EstrategiaModeloLocal,
    }

    if nombre_estrategia not in estrategias:
        return jsonify(
            error="Estrategia inválida. Opciones: gemini, openai o local"
        ), 400

    pregunta = db.session.get(Pregunta, pregunta_id)

    if pregunta is None:
        return jsonify(error="Pregunta inexistente"), 404

    agente = db.session.query(AgenteIA).first()

    if agente is None:
        agente = AgenteIA(nombre="Agente IA")
        db.session.add(agente)
        db.session.flush()

    agente.establecerEstrategia(estrategias[nombre_estrategia]())

    cuerpo = agente.generarRespuesta(pregunta)

    respuesta = Respuesta(
        cuerpo=cuerpo,
        fechaPubli=date.today().isoformat(),
        pregunta_id=pregunta.id
    )

    respuesta.establecerAutor(agente)

    db.session.add(respuesta)
    db.session.commit()

    return jsonify(
        mensaje="Respuesta generada por el agente IA",
        id=respuesta.id,
        pregunta_id=pregunta.id,
        cuerpo=respuesta.cuerpo,
        autor_id=respuesta.autor_id,
        autor_tipo=respuesta.autor_tipo,
        estrategia=nombre_estrategia
    ), 201


@respuestas_bp.post("/automatizacion/ia/preguntas-sin-respuesta")
def revisar_preguntas_sin_respuesta():
    preguntas_procesadas = procesar_preguntas_sin_respuesta()

    return jsonify(
        mensaje="Revisión de preguntas finalizada",
        cantidad=len(preguntas_procesadas),
        preguntas_procesadas=preguntas_procesadas
    ), 200


@respuestas_bp.patch(
    "/preguntas/<int:pregunta_id>/respuestas/<int:respuesta_id>/aceptar"
)
def aceptar_respuesta(pregunta_id, respuesta_id):
    datos = request.get_json()

    if not datos or datos.get("usuario_id") is None:
        return jsonify(error="Se requiere el usuario que acepta"), 400

    pregunta = db.session.get(Pregunta, pregunta_id)
    respuesta = db.session.get(Respuesta, respuesta_id)

    if pregunta is None or respuesta is None:
        return jsonify(error="Pregunta o respuesta inexistente"), 404

    if pregunta.usuario_id != datos["usuario_id"]:
        return jsonify(
            error="Solo el autor de la pregunta puede aceptar respuestas"
        ), 403

    if respuesta.pregunta_id != pregunta.id:
        return jsonify(
            error="La respuesta no pertenece a esta pregunta"
        ), 400

    respuesta.aceptada = True
    db.session.commit()

    return jsonify(
        mensaje="Respuesta aceptada correctamente",
        respuesta_id=respuesta.id,
        aceptada=respuesta.aceptada
    ), 200
