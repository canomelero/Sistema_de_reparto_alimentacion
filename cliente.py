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

from . import db
# import Sistema_de_reparto_alimentacion as Sistema_de_reparto_alimentacion

import psycopg2
import psycopg2.extras as extras

# Creación de blueprint para que todas las rutas de /cliente estén agrupadas
bp = Blueprint("cliente", __name__)


# Ruta para listar los clientes de la base de datos
@bp.route('/clientes')
def listar():
    """
    Listar todos los clientes de la app
    """
    cursor = db.get_db_cursor()

    if(cursor != None):
        cursor.execute(
            "SELECT * FROM cliente"
        )

        clientes = cursor.fetchall()

    return render_template('./cliente/cliente.html', clientes = clientes)


# Ruta para registrar (guardar) clientes en la base de datos
@bp.route("/registro", methods = ["POST"])
def registro():
    """
    Registro de un nuevo cliente
    """
    nombre = request.form["nombre-cliente"]
    email = request.form["email"]
    direccion = request.form["direccion"]
    telf = request.form["telefono"]
    
    if nombre and email and direccion and telf:
        conexion = db.get_db()
        cursor = db.get_db_cursor()

        cursor.execute(
            "INSERT INTO cliente (nombre, email, direccion, telefono) VALUES (%s, %s, %s, %s)",
            (nombre, email, direccion, telf)
        )

        conexion.commit()
        cursor.close()

    return redirect(url_for("cliente.listar"))


# Ruta para eliminar un cliente de la base de datos
@bp.route("/borrar/<int:id>")
def borrar(id):
    """Borrar un cliente de la base de datos

    Parameters
    ----------
    id : int
        Identificador del cliente que se va a eliminar
    """
    conexion = db.get_db()
    cursor = db.get_db_cursor()

    cursor.execute(
        "DELETE FROM cliente WHERE id = %s",
        (id,)
    )

    conexion.commit()
    cursor.close()

    return redirect(url_for("cliente.listar"))


# Ruta para eliminar un cliente de la base de datos
@bp.route("/actualizar/<int:id>", methods = ["POST"])
def actualizar(id):
    """Actualiza los datos de un cliente de la base de datos

    Parameters
    ----------
    id : int
        Identificador del cliente que se va a eliminar
    """
    nombre = request.form["nombre-cliente"]
    email = request.form["email"]
    direccion = request.form["direccion"]
    telf = request.form["telefono"]

    conexion = db.get_db()
    cursor = db.get_db_cursor()

    cursor.execute(
        "UPDATE cliente SET nombre = %s, email = %s, direccion = %s, telefono = %s WHERE id = %s",
        (nombre, email, direccion, telf, id)
    )

    conexion.commit()
    cursor.close()

    return redirect(url_for("cliente.listar"))