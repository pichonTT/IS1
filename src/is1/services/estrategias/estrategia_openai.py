from is1.services.estrategias.generador_respuesta_strategy import (
    GeneradorRespuestaStrategy,
)


class EstrategiaOpenAI(GeneradorRespuestaStrategy):

    def generarRespuesta(self, p):
        return (
            f"[Respuesta simulada de OpenAI]\n"
            f"Sobre la pregunta '{p.titulo}': "
            "una posible solución es estudiar los datos disponibles, "
            "evaluar las alternativas y justificar la respuesta "
            "con los conceptos correspondientes."
        )