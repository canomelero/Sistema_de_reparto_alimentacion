import functools

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

import db as db
import app as app

import psycopg2
import psycopg2.extras as extras

# Creación de blueprint para que todas las rutas de /cliente estén agrupadas
bp = Blueprint("cliente", __name__, url_prefix="/cliente")


# Ruta para registrar (guardar) usuarios en la base de datos
@bp.route("/registro", methods = ["POST"])
def registro():
    """
    Registro de un nuevo cliente
    """
    nombre = request.form["nombre-cliente"]
    email = request.form["email"]
    direccion = request.form["direccion"]
    telf = request.form["telefono"]

    if not nombre:
        error = "Es obligatorio introducir el nombre"

    if not email:
        error = "Es obligatorio introducir el email"

    if not direccion:
        error = "Es obligatorio introducir la dirección"
    
    if not telf:
        error = "Es obligatorio introducir el teléfono"
    
    if error is not None:
        flash(error)
    else:
        conexion = db.get_db()
        cursor = db.get_db_cursor()

        cursor.execute(
            "INSERT INTO cliente (nombre, email, direccion, telefono) VALUES (%s, %s, %s, %s)",
            "(nombre, email, direccion, telf)"
        )

        conexion.commit()
        cursor.close()

    return render_template(url_for("app.cliente"))