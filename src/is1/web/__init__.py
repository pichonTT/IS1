
from datetime import datetime

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from sqlalchemy import func
from werkzeug.security import check_password_hash, generate_password_hash

from is1.extensions import db
from is1.models import (
    Categoria,
    Etiqueta,
    Pregunta,
    Respuesta,
    RolUsuario,
    Tipo_Voto,
    Usuario,
    Voto,
)
from is1.services.automatizacion_ia import generar_respuesta_ia

web_bp = Blueprint("web", __name__)


def usuario_actual():
    usuario_id = session.get("usuario_id")
    if usuario_id is None:
        return None
    return db.session.get(Usuario, usuario_id)


@web_bp.app_context_processor
def inyectar_usuario():
    return {"usuario_actual": usuario_actual()}


@web_bp.route("/")
def inicio():
    busqueda = request.args.get("q", "").strip()

    consulta = Pregunta.query
    if busqueda:
        consulta = consulta.filter(
            func.lower(Pregunta.titulo).contains(busqueda.lower())
            | func.lower(Pregunta.cuerpo).contains(busqueda.lower())
        )

    preguntas = consulta.order_by(Pregunta.id.desc()).all()
    return render_template(
        "index.html",
        preguntas=preguntas,
        busqueda=busqueda,
    )


@web_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        contrasena = request.form.get("contrasena", "")

        if not email or not contrasena:
            flash("Completá el correo y la contraseña.", "error")
            return render_template("registro.html")

        if Usuario.query.filter_by(email=email).first():
            flash("Ya existe una cuenta con ese correo.", "error")
            return render_template("registro.html")

        usuario = Usuario(
            email=email,
            contrasena=generate_password_hash(contrasena),
            rol=RolUsuario.GENERAL,
        )
        db.session.add(usuario)
        db.session.commit()

        session["usuario_id"] = usuario.id
        flash("Tu cuenta fue creada correctamente.", "success")
        return redirect(url_for("web.inicio"))

    return render_template("registro.html")


@web_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        contrasena = request.form.get("contrasena", "")

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario is None or not check_password_hash(
            usuario.contrasena,
            contrasena,
        ):
            flash("Correo o contraseña incorrectos.", "error")
            return render_template("login.html")

        session["usuario_id"] = usuario.id
        flash("Iniciaste sesión correctamente.", "success")
        return redirect(url_for("web.inicio"))

    return render_template("login.html")


@web_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Cerraste sesión.", "success")
    return redirect(url_for("web.inicio"))


@web_bp.route("/preguntas/nueva", methods=["GET", "POST"])
def nueva_pregunta():
    usuario = usuario_actual()
    if usuario is None:
        flash("Iniciá sesión para publicar una pregunta.", "error")
        return redirect(url_for("web.login"))

    categorias = Categoria.query.order_by(Categoria.nombre).all()

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        cuerpo = request.form.get("cuerpo", "").strip()
        categoria_id = request.form.get("categoria_id", type=int)
        nombres_etiquetas = request.form.get("etiquetas", "").split(",")
        usar_ia = request.form.get("ia_help") == "on"

        categoria = db.session.get(Categoria, categoria_id)

        if not titulo or not cuerpo or categoria is None:
            flash("Completá el título, el contenido y la categoría.", "error")
            return render_template(
                "nueva_pregunta.html",
                categorias=categorias,
            )

        pregunta = Pregunta(
            titulo=titulo,
            cuerpo=cuerpo,
            fechaPubli=datetime.now().isoformat(timespec="seconds"),
            usuario_id=usuario.id,
            categoria_id=categoria.id,
        )

        for nombre in nombres_etiquetas:
            nombre = nombre.strip()
            if nombre:
                etiqueta = Etiqueta.query.filter(
                    func.lower(Etiqueta.nombre) == nombre.lower()
                ).first()
                if etiqueta is None:
                    etiqueta = Etiqueta(nombre=nombre)
                    db.session.add(etiqueta)
                pregunta.etiquetas.append(etiqueta)

        if usar_ia:
            etiqueta_ia = Etiqueta.query.filter(
                func.lower(Etiqueta.nombre) == "ia-help"
            ).first()
            if etiqueta_ia is None:
                etiqueta_ia = Etiqueta(nombre="ia-help")
                db.session.add(etiqueta_ia)
            if etiqueta_ia not in pregunta.etiquetas:
                pregunta.etiquetas.append(etiqueta_ia)

        db.session.add(pregunta)
        db.session.commit()

        if usar_ia:
            generar_respuesta_ia(pregunta)

        flash("Tu pregunta fue publicada.", "success")
        return redirect(url_for("web.ver_pregunta", pregunta_id=pregunta.id))

    return render_template("nueva_pregunta.html", categorias=categorias)


@web_bp.route("/pregunta/<int:pregunta_id>")
def ver_pregunta(pregunta_id):
    pregunta = db.session.get(Pregunta, pregunta_id)
    if pregunta is None:
        flash("La pregunta no existe.", "error")
        return redirect(url_for("web.inicio"))

    return render_template("pregunta.html", pregunta=pregunta)


@web_bp.route("/pregunta/<int:pregunta_id>/responder", methods=["POST"])
def responder(pregunta_id):
    usuario = usuario_actual()
    if usuario is None:
        flash("Iniciá sesión para responder.", "error")
        return redirect(url_for("web.login"))

    pregunta = db.session.get(Pregunta, pregunta_id)
    cuerpo = request.form.get("cuerpo", "").strip()

    if pregunta is None or not cuerpo:
        flash("No se pudo publicar la respuesta.", "error")
        return redirect(url_for("web.inicio"))

    respuesta = Respuesta(
        cuerpo=cuerpo,
        fechaPubli=datetime.now().isoformat(timespec="seconds"),
        pregunta_id=pregunta.id,
    )
    respuesta.establecerAutor(usuario)

    db.session.add(respuesta)
    db.session.commit()

    flash("Tu respuesta fue publicada.", "success")
    return redirect(url_for("web.ver_pregunta", pregunta_id=pregunta.id))


@web_bp.route("/pregunta/<int:pregunta_id>/ia", methods=["POST"])
def respuesta_ia(pregunta_id):
    usuario = usuario_actual()
    if usuario is None:
        flash("Iniciá sesión para solicitar asistencia de IA.", "error")
        return redirect(url_for("web.login"))

    pregunta = db.session.get(Pregunta, pregunta_id)
    if pregunta is None:
        flash("La pregunta no existe.", "error")
        return redirect(url_for("web.inicio"))

    try:
        respuesta = generar_respuesta_ia(pregunta)
        if respuesta is None:
            flash("Esta pregunta ya tiene una respuesta de IA.", "error")
        else:
            flash("La respuesta de IA fue generada.", "success")
    except ValueError as error:
        flash(str(error), "error")

    return redirect(url_for("web.ver_pregunta", pregunta_id=pregunta.id))


@web_bp.route(
    "/pregunta/<int:pregunta_id>/aceptar/<int:respuesta_id>",
    methods=["POST"],
)
def aceptar_respuesta(pregunta_id, respuesta_id):
    usuario = usuario_actual()
    pregunta = db.session.get(Pregunta, pregunta_id)
    respuesta = db.session.get(Respuesta, respuesta_id)

    if usuario is None:
        flash("Iniciá sesión para realizar esta acción.", "error")
    elif pregunta is None or respuesta is None:
        flash("No se encontró la pregunta o respuesta.", "error")
    elif pregunta.usuario_id != usuario.id:
        flash("Solo quien publicó la pregunta puede aceptar respuestas.", "error")
    elif respuesta.pregunta_id != pregunta.id:
        flash("La respuesta no pertenece a esta pregunta.", "error")
    else:
        for otra in pregunta.respuestas:
            otra.aceptada = otra.id == respuesta.id
        db.session.commit()
        flash("Respuesta aceptada correctamente.", "success")

    if pregunta is None:
        return redirect(url_for("web.inicio"))
    return redirect(url_for("web.ver_pregunta", pregunta_id=pregunta.id))


def registrar_voto_web(elemento, campo, tipo):
    usuario = usuario_actual()
    if usuario is None:
        flash("Iniciá sesión para votar.", "error")
        return

    try:
        tipo_voto = Tipo_Voto(tipo.upper())
    except (ValueError, AttributeError):
        flash("El voto debe ser positivo o negativo.", "error")
        return

    filtros = {"usuario_id": usuario.id, campo: elemento.id}
    voto = Voto.query.filter_by(**filtros).first()

    if voto is None:
        voto = Voto(
            usuario_id=usuario.id,
            tipo=tipo_voto,
            fecha=datetime.now().isoformat(timespec="seconds"),
            pregunta_id=elemento.id if campo == "pregunta_id" else None,
            respuesta_id=elemento.id if campo == "respuesta_id" else None,
        )
        db.session.add(voto)
    else:
        voto.tipo = tipo_voto
        voto.fecha = datetime.now().isoformat(timespec="seconds")

    db.session.commit()
    flash("Tu voto fue registrado.", "success")


@web_bp.route("/pregunta/<int:pregunta_id>/votar", methods=["POST"])
def votar_pregunta(pregunta_id):
    pregunta = db.session.get(Pregunta, pregunta_id)
    if pregunta is None:
        flash("La pregunta no existe.", "error")
        return redirect(url_for("web.inicio"))

    registrar_voto_web(
        pregunta,
        "pregunta_id",
        request.form.get("tipo", ""),
    )
    return redirect(url_for("web.ver_pregunta", pregunta_id=pregunta.id))


@web_bp.route("/respuesta/<int:respuesta_id>/votar", methods=["POST"])
def votar_respuesta(respuesta_id):
    respuesta = db.session.get(Respuesta, respuesta_id)
    if respuesta is None:
        flash("La respuesta no existe.", "error")
        return redirect(url_for("web.inicio"))

    registrar_voto_web(
        respuesta,
        "respuesta_id",
        request.form.get("tipo", ""),
    )
    return redirect(
        url_for("web.ver_pregunta", pregunta_id=respuesta.pregunta_id)
    )
