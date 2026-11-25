
import os

from apscheduler.schedulers.background import BackgroundScheduler

_programador = None


def revisar_preguntas_automaticamente(app):
    from is1.services.automatizacion_ia import (
        procesar_preguntas_sin_respuesta,
    )

    with app.app_context():
        try:
            procesadas = procesar_preguntas_sin_respuesta()
            app.logger.info(
                "Revisión automática finalizada. Preguntas procesadas: %s",
                procesadas
            )
        except Exception:
            app.logger.exception("Error en la revisión automática de IA")


def iniciar_programador(app):
    global _programador

    if app.config.get("TESTING"):
        return

    if app.config.get("SCHEDULER_ENABLED") is False:
        return

    # Evita iniciar dos programadores con el recargador de Flask en modo debug.
    if app.debug and os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        return

    if _programador is not None and _programador.running:
        return

    _programador = BackgroundScheduler(
        timezone="America/Argentina/Cordoba"
    )

    _programador.add_job(
        revisar_preguntas_automaticamente,
        trigger="interval",
        hours=1,
        args=[app],
        id="revision_preguntas_ia",
        replace_existing=True,
        max_instances=1,
        coalesce=True
    )

    _programador.start()
    app.logger.info("Programador automático de IA iniciado")
