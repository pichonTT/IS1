
from is1.extensions import db
from is1.models.tipo_voto import Tipo_Voto


class Voto(db.Model):
    __tablename__ = "voto"

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(
        db.Enum(Tipo_Voto),
        nullable=False
    )
    fecha = db.Column(db.String, nullable=False)

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuario.id"),
        nullable=False
    )

    pregunta_id = db.Column(
        db.Integer,
        db.ForeignKey("pregunta.id"),
        nullable=False
    )
    usuario = db.relationship("Usuario", back_populates="votos")
    pregunta = db.relationship("Pregunta", back_populates="votos")