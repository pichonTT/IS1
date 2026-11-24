from abc import ABC, abstractmethod


class Autor(ABC):

    @abstractmethod
    def obtenerIdentificador(self):
        pass