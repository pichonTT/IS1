
from is1.extensions import db


pregunta_etiqueta = db.Table(
    "pregunta_etiqueta",
    db.Column("pregunta_id", db.Integer, db.ForeignKey("pregunta.id"), primary_key=True),
    db.Column("etiqueta_id", db.Integer, db.ForeignKey("etiqueta.id"), primary_key=True),
)


class Pregunta(db.Model):
    __tablename__ = "pregunta"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String, nullable=False)
    cuerpo = db.Column(db.String, nullable=False)
    fechaPubli = db.Column(db.String, nullable=False)

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"), nullable=False)

    etiquetas = db.relationship(
        "Etiqueta",
        secondary=pregunta_etiqueta,
        back_populates="preguntas"
    )

    respuestas = db.relationship(
        "Respuesta",
        back_populates="pregunta"
    )
