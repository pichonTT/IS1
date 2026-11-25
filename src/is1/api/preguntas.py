
from datetime import datetime

from flask import Blueprint, jsonify, request

from is1.extensions import db
from is1.models import Categoria, Etiqueta, Pregunta, Usuario
from is1.services.automatizacion_ia import generar_respuesta_ia

preguntas_bp = Blueprint("preguntas", __name__)


@preguntas_bp.post("/preguntas")
def crear_pregunta():
    datos = request.get_json()

    if not datos:
        return jsonify(error="Se requiere un JSON"), 400

    titulo = datos.get("titulo")
    cuerpo = datos.get("cuerpo")
    fecha = datos.get("fechaPubli")
    usuario_id = datos.get("usuario_id")
    categoria_id = datos.get("categoria_id")
    etiquetas_ids = datos.get("etiquetas_ids", [])

    if not titulo or not cuerpo or not fecha:
        return jsonify(error="Faltan datos obligatorios"), 400

    if not isinstance(etiquetas_ids, list):
        return jsonify(error="Las etiquetas deben ser una lista"), 400

    try:
        fecha_publicacion = datetime.fromisoformat(fecha)
    except (ValueError, TypeError):
        return jsonify(error="La fecha debe tener formato ISO válido"), 400

    ahora = datetime.now()

    if fecha_publicacion.tzinfo is not None:
        fecha_publicacion = fecha_publicacion.astimezone().replace(
            tzinfo=None
        )
    elif len(fecha) == 10 and fecha_publicacion.date() == ahora.date():
        # Si llega solamente la fecha de hoy, usamos la hora real de publicación.
        fecha_publicacion = ahora

    usuario = db.session.get(Usuario, usuario_id)
    categoria = db.session.get(Categoria, categoria_id)

    if usuario is None:
        return jsonify(error="Usuario inexistente"), 404

    if categoria is None:
        return jsonify(error="Categoría inexistente"), 404

    etiquetas = []

    for etiqueta_id in etiquetas_ids:
        etiqueta = db.session.get(Etiqueta, etiqueta_id)

        if etiqueta is None:
            return jsonify(error=f"Etiqueta {etiqueta_id} inexistente"), 404

        etiquetas.append(etiqueta)

    pregunta = Pregunta(
        titulo=titulo,
        cuerpo=cuerpo,
        fechaPubli=fecha_publicacion.isoformat(timespec="seconds"),
        usuario=usuario,
        categoria=categoria,
        etiquetas=etiquetas
    )

    db.session.add(pregunta)
    db.session.commit()

    respuesta_ia = None

    if any(etiqueta.nombre.lower() == "ia-help" for etiqueta in etiquetas):
        respuesta_ia = generar_respuesta_ia(pregunta)

    return jsonify(
        mensaje="Pregunta creada correctamente",
        id=pregunta.id,
        titulo=pregunta.titulo,
        usuario_id=pregunta.usuario_id,
        categoria_id=pregunta.categoria_id,
        etiquetas_ids=[etiqueta.id for etiqueta in pregunta.etiquetas],
        respuesta_ia_id=(
            respuesta_ia.id if respuesta_ia is not None else None
        )
    ), 201


@preguntas_bp.get("/preguntas")
def listar_preguntas():
    preguntas = db.session.query(Pregunta).all()

    resultado = []

    for pregunta in preguntas:
        resultado.append({
            "id": pregunta.id,
            "titulo": pregunta.titulo,
            "cuerpo": pregunta.cuerpo,
            "fechaPubli": pregunta.fechaPubli,
            "usuario_id": pregunta.usuario_id,
            "categoria_id": pregunta.categoria_id,
            "etiquetas": [
                {"id": etiqueta.id, "nombre": etiqueta.nombre}
                for etiqueta in pregunta.etiquetas
            ],
            "respuestas": [
                {
                    "id": respuesta.id,
                    "cuerpo": respuesta.cuerpo,
                    "fechaPubli": respuesta.fechaPubli,
                    "aceptada": respuesta.aceptada,
                    "autor_id": respuesta.autor_id,
                    "autor_tipo": respuesta.autor_tipo
                }
                for respuesta in pregunta.respuestas
            ]
        })

    return jsonify(resultado), 200


@preguntas_bp.get("/preguntas/<int:pregunta_id>")
def consultar_pregunta(pregunta_id):
    pregunta = db.session.get(Pregunta, pregunta_id)

    if pregunta is None:
        return jsonify(error="Pregunta inexistente"), 404

    return jsonify(
        id=pregunta.id,
        titulo=pregunta.titulo,
        cuerpo=pregunta.cuerpo,
        fechaPubli=pregunta.fechaPubli,
        usuario_id=pregunta.usuario_id,
        categoria_id=pregunta.categoria_id,
        etiquetas=[
            {"id": etiqueta.id, "nombre": etiqueta.nombre}
            for etiqueta in pregunta.etiquetas
        ],
        respuestas=[
            {
                "id": respuesta.id,
                "cuerpo": respuesta.cuerpo,
                "fechaPubli": respuesta.fechaPubli,
                "aceptada": respuesta.aceptada,
                "autor_id": respuesta.autor_id,
                "autor_tipo": respuesta.autor_tipo
            }
            for respuesta in pregunta.respuestas
        ]
    ), 200
