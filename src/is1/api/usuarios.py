from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash

from is1.extensions import db
from is1.models import RolUsuario, Usuario

usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.post("/usuarios")
def registrar_usuario():
    datos = request.get_json()

    if not datos:
        return jsonify(error="Se requiere un JSON"), 400

    email = datos.get("email")
    contrasena = datos.get("contrasena")

    if not email or not contrasena:
        return jsonify(error="Email y contraseña son obligatorios"), 400

    existente = db.session.query(Usuario).filter_by(email=email).first()

    if existente:
        return jsonify(error="El email ya está registrado"), 409

    usuario = Usuario(
        email=email,
        contrasena=generate_password_hash(contrasena),
        rol=RolUsuario.GENERAL
    )

    db.session.add(usuario)
    db.session.commit()

    return jsonify(
        mensaje="Usuario registrado correctamente",
        id=usuario.id,
        email=usuario.email,
        rol=usuario.rol.value
    ), 201