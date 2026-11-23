from abc import ABC, abstractmethod


class GeneradorRespuestaStrategy(ABC):

    @abstractmethod
    def generarRespuesta(self, p):
        pass