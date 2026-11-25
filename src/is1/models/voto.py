
from is1.extensions import db
from is1.models.tipo_voto import Tipo_Voto


class Voto(db.Model):
    __tablename__ = "voto"

    __table_args__ = (
        db.UniqueConstraint(
            "usuario_id",
            "pregunta_id",
            name="uq_voto_usuario_pregunta",
        ),
        db.UniqueConstraint(
            "usuario_id",
            "respuesta_id",
            name="uq_voto_usuario_respuesta",
        ),
        db.CheckConstraint(
            """
            (pregunta_id IS NOT NULL AND respuesta_id IS NULL)
            OR
            (pregunta_id IS NULL AND respuesta_id IS NOT NULL)
            """,
            name="ck_voto_un_solo_destino",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)

    tipo = db.Column(
        db.Enum(Tipo_Voto),
        nullable=False,
    )

    fecha = db.Column(db.String, nullable=False)

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuario.id"),
        nullable=False,
    )

    pregunta_id = db.Column(
        db.Integer,
        db.ForeignKey("pregunta.id"),
        nullable=True,
    )

    respuesta_id = db.Column(
        db.Integer,
        db.ForeignKey("respuesta.id"),
        nullable=True,
    )

    usuario = db.relationship(
        "Usuario",
        back_populates="votos",
    )

    pregunta = db.relationship(
        "Pregunta",
        back_populates="votos",
    )

    respuesta = db.relationship(
        "Respuesta",
        back_populates="votos",
    )
