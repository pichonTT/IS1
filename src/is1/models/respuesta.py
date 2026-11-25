
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

    autor_id = db.Column(db.Integer, nullable=False)
    autor_tipo = db.Column(db.String(20), nullable=False)

    pregunta = db.relationship(
        "Pregunta",
        back_populates="respuestas"
    )

    votos = db.relationship(
        "Voto",
        back_populates="respuesta"
    )

    @property
    def autor(self):
        from is1.models.agente_ia import AgenteIA
        from is1.models.usuario import Usuario

        if self.autor_tipo == "USUARIO":
            return db.session.get(Usuario, self.autor_id)

        if self.autor_tipo == "AGENTE_IA":
            return db.session.get(AgenteIA, self.autor_id)

        return None

    def establecerAutor(self, autor):
        from is1.models.agente_ia import AgenteIA
        from is1.models.usuario import Usuario

        if isinstance(autor, Usuario):
            self.autor_id = autor.id
            self.autor_tipo = "USUARIO"

        elif isinstance(autor, AgenteIA):
            self.autor_id = autor.id
            self.autor_tipo = "AGENTE_IA"

        else:
            raise TypeError("El autor debe ser Usuario o AgenteIA")
