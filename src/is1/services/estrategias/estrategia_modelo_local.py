from is1.services.estrategias.generador_respuesta_strategy import (
    GeneradorRespuestaStrategy,
)


class EstrategiaModeloLocal(GeneradorRespuestaStrategy):

    def generarRespuesta(self, p):
        return (
            f"[Respuesta simulada de Modelo Local]\n"
            f"Sobre la pregunta '{p.titulo}': "
            "te propongo revisar el problema paso a paso, "
            "considerar los datos disponibles y elaborar "
            "una respuesta fundamentada."
        )