from is1.services.estrategias.generador_respuesta_strategy import (
    GeneradorRespuestaStrategy,
)


class EstrategiaGemini(GeneradorRespuestaStrategy):

    def generarRespuesta(self, p):
        return (
            f"[Respuesta simulada de Gemini]\n"
            f"Sobre la pregunta '{p.titulo}': "
            "te recomiendo analizar el problema por partes, "
            "identificar los conceptos principales y buscar "
            "una solución que responda a lo planteado."
        )