from is1.extensions import db
from is1.models.autor import Autor


class AgenteIA(db.Model, Autor):
    __tablename__ = "agente_ia"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)

    def __init__(self, nombre, estrategia=None):
        self.nombre = nombre
        self.estrategia = estrategia

    def establecerEstrategia(self, estrategia):
        self.estrategia = estrategia

    def generarRespuesta(self, p):
        if self.estrategia is None:
            raise ValueError("No se configuró una estrategia de generación")

        return self.estrategia.generarRespuesta(p)

    def obtenerIdentificador(self):
        return self.id