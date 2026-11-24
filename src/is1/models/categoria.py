from is1.extensions import db


class Categoria(db.Model):
    __tablename__ = "categoria"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)

    preguntas = db.relationship(
        "Pregunta",
        back_populates="categoria"
    )