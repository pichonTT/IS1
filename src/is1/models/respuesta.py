from is1.extensions import db


class Respuesta(db.Model):
    __tablename__ = "respuesta"

    id = db.Column(db.Integer, primary_key=True)
    cuerpo = db.Column(db.String, nullable=False)
    fechaPubli = db.Column(db.String, nullable=False)
    aceptada = db.Column(db.Boolean, nullable=False, default=False)

    pregunta_id = db.Column(
        db.Integer,
        db.ForeignKey("pregunta.id"),
        nullable=False
    )

    pregunta = db.relationship(
        "Pregunta",
        back_populates="respuestas"
    )