from is1.extensions import db
from is1.models.pregunta import pregunta_etiqueta


class Etiqueta(db.Model):
    __tablename__ = "etiqueta"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)

    preguntas = db.relationship(
        "Pregunta",
        secondary=pregunta_etiqueta,
        back_populates="etiquetas"
    )