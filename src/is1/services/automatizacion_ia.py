
from datetime import datetime, timedelta

from is1.extensions import db
from is1.models import AgenteIA, Pregunta, Respuesta
from is1.services.estrategias.estrategia_gemini import EstrategiaGemini
from is1.services.estrategias.estrategia_modelo_local import (
    EstrategiaModeloLocal,
)
from is1.services.estrategias.estrategia_openai import EstrategiaOpenAI

ESTRATEGIAS = {
    "gemini": EstrategiaGemini,
    "openai": EstrategiaOpenAI,
    "local": EstrategiaModeloLocal,
}

HORAS_ESPERA = 24


def ya_tiene_respuesta_ia(pregunta):
    return any(
        respuesta.autor_tipo == "AGENTE_IA"
        for respuesta in pregunta.respuestas
    )


def generar_respuesta_ia(pregunta, nombre_estrategia="gemini"):
    if nombre_estrategia not in ESTRATEGIAS:
        raise ValueError("Estrategia de IA inválida")

    if ya_tiene_respuesta_ia(pregunta):
        return None

    agente = db.session.query(AgenteIA).first()

    if agente is None:
        agente = AgenteIA(nombre="Agente IA")
        db.session.add(agente)
        db.session.flush()

    agente.establecerEstrategia(ESTRATEGIAS[nombre_estrategia]())

    respuesta = Respuesta(
        cuerpo=agente.generarRespuesta(pregunta),
        fechaPubli=datetime.now().isoformat(timespec="seconds"),
        pregunta_id=pregunta.id
    )

    respuesta.establecerAutor(agente)

    db.session.add(respuesta)
    db.session.commit()

    return respuesta


def tiene_etiqueta_ia_help(pregunta):
    return any(
        etiqueta.nombre.lower() == "ia-help"
        for etiqueta in pregunta.etiquetas
    )


def procesar_preguntas_con_ia_help():
    preguntas = db.session.query(Pregunta).all()
    procesadas = []

    for pregunta in preguntas:
        if tiene_etiqueta_ia_help(pregunta):
            respuesta = generar_respuesta_ia(pregunta)

            if respuesta is not None:
                procesadas.append(pregunta.id)

    return procesadas


def procesar_preguntas_sin_respuesta():
    preguntas = db.session.query(Pregunta).all()
    limite = datetime.now() - timedelta(hours=HORAS_ESPERA)
    procesadas = []

    for pregunta in preguntas:
        if pregunta.respuestas:
            continue

        try:
            fecha_publicacion = datetime.fromisoformat(
                pregunta.fechaPubli
            )

            if fecha_publicacion.tzinfo is not None:
                fecha_publicacion = fecha_publicacion.astimezone().replace(
                    tzinfo=None
                )

        except (ValueError, TypeError):
            continue

        if fecha_publicacion <= limite:
            respuesta = generar_respuesta_ia(pregunta)

            if respuesta is not None:
                procesadas.append(pregunta.id)

    return procesadas
