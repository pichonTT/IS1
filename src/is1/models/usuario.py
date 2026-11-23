from is1.extensions import db
from is1.models.rol_usuario import RolUsuario


class Usuario(db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    rol = db.Column(db.Enum(RolUsuario), nullable=False)
    contrasena = db.Column(db.String, nullable=False)

    preguntas = db.relationship(
        "Pregunta",
        back_populates="usuario"
    )

    votos = db.relationship(
        "Voto",
        back_populates="usuario"
    )