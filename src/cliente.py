from flask import Blueprint, redirect, render_template, request, url_for
from .. import db


# Creación de blueprint para que todas las rutas de /cliente estén agrupadas
bp = Blueprint("cliente", __name__)


# @bp.route("/")
# def index():
#     return render_template("./base.html")

# Ruta para listar los clientes de la base de datos
@bp.route('/clientes', methods = ["GET"])
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

    return render_template('cliente/cliente.html', clientes = clientes)


# Ruta para registrar (guardar) clientes en la base de datos
@bp.route("/registro", methods = ["POST"])
def registro():
    """
    Registro de un nuevo cliente
    """
    nombre = request.form["nombre"]
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
@bp.route("/eliminar/<int:id>", methods = ["GET"])
def eliminar(id):
    """Borrar un cliente de la base de datos

    Parameters
    ----------
    id : int
        Identificador del cliente que se va a eliminar
    """
    conexion = db.get_db()
    cursor = db.get_db_cursor()

    cursor.execute(
        "DELETE FROM cliente WHERE id_cliente = %s",
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
        "UPDATE cliente SET nombre = %s, email = %s, direccion = %s, telefono = %s WHERE id_cliente = %s",
        (nombre, email, direccion, telf, id)
    )

    conexion.commit()
    cursor.close()

    return redirect(url_for("cliente.listar"))
    
    # if request.method == "POST":
    #     nombre = request.form["nombre-cliente"]
    #     email = request.form["email"]
    #     direccion = request.form["direccion"]
    #     telf = request.form["telefono"]

    #     conexion = db.get_db()
    #     cursor = db.get_db_cursor()

    #     cursor.execute(
    #         "UPDATE cliente SET nombre = %s, email = %s, direccion = %s, telefono = %s WHERE id_cliente = %s",
    #         (nombre, email, direccion, telf, id)
    #     )

    #     conexion.commit()
    #     cursor.close()

    #     return redirect(url_for("cliente.listar"))
    
    # return render_template("./cliente/cliente.html", cliente = cliente)