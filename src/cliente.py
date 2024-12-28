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
    nombre = request.form["nombre"]
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


# Ruta para listar los pedidos de un cliente
@bp.route("/pedidos/<int:id>", methods = ["GET"])
def pedidos(id):
    cursor = db.get_db_cursor()

    # Hay que filtrar primero por cliente y luego mostrar los pedidos del cliente

    cursor.execute(
        "SELECT * FROM pedido_incluye_reparte WHERE numero_pedido = %s",
        (id,)
    )

    pedidos = cursor.fetchall()

    return render_template("cliente/lista_pedidos.html", pedidos = pedidos)


# Ruta para listar las facturas de un cliente
@bp.route("/facturas/<int:id>", methods = ["GET"])
def facturas(id):
    cursor = db.get_db_cursor()

    # Hay que filtrar primero por cliente y luego mostrar los pedidos del cliente

    cursor.execute(
        "SELECT * FROM factura WHERE numero_pedido = %s",
        (id,)
    )

    facturas = cursor.fetchall()

    return render_template("cliente/lista_facturas.html", facturas = facturas)


# Ruta para realizar un pedido
# Se clicka sobre el nombre del cliente
# Se redirige a un endpoint de resturante.py que liste los restaurantes disponibles
# Se clicka sobre un restaurante y muestra los platos que oferta ese restaurante
# Se clicka sobre la opción "pedir" que habrá para cada plato disponible
# El pedido clickado se guarda en la tabla pedido 
# El pedido se podrá pagar y una vez pagado se guarda en la tabla factura


