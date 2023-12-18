# Va a contener todas las vistas y autenticacion de ususarios
from flask import (
    Blueprint, render_template, request, url_for, redirect, flash, session , g
  )

from werkzeug.security import generate_password_hash, check_password_hash

from .models import User

from todor import db


bp = Blueprint("auth", __name__, url_prefix="/auth")

#Con GET y POST obtenemos los datos del formulario
@bp.route("/register", methods = ("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form ["username"]
        password = request.form ["password"]

        # Cremos un objeto del modelo user
        user = User(username, generate_password_hash(password))

        error = None

        # Buscamos en la base de datos un nombre de ususario que sea igual al usuario que intetamos registrar 
        user_name = User.query.filter_by(username = username).first()

        #Si el usuario no se encuentra que se registre como usuario nuevo
        if user_name == None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        else:
            error = f"El usuario {username} ya esta registrado"
        flash(error)

    return render_template("auth/register.html")

@bp.route("/login", methods = ("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form ["username"]
        password = request.form ["password"]

        # Cremos un objeto del modelo user
        user = User(username, generate_password_hash(password))

        error = None

        #Validar datos
        user = User.query.filter_by(username = username).first()
        if user == None:
            error = "Nombre de usuario incorrecto"
        elif not check_password_hash(user.password, password):
            error = "Contraseña incorrecta"

        #Inciar sesión 
        if error == None:
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("todo.index"))
        flash(error)

    return render_template("auth/login.html")

# Mantener la sesion iniciada
@bp.before_app_request
def load_logger_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None

    else:
        g.user = User.query.get_or_404(user_id)
    
@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# verificar a que parte de la app se requiere inicio de sesion si no a ingresado un usuario valido 
# redirecciona a login
import functools

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view