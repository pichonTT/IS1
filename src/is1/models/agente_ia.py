from is1.extensions import db


class AgenteIA(db.Model):
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