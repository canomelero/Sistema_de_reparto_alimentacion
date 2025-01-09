from flask import Blueprint, redirect, render_template, request, url_for
from .. import db


# Creación de blueprint para que todas las rutas de /cliente estén agrupadas
bp = Blueprint("cliente", __name__)


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

    return redirect(url_for("home"))


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

    return redirect(url_for("home"))


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

    return redirect(url_for("home"))


# Ruta para listar los pedidos de un cliente
@bp.route("/pedidos/<int:id>", methods = ["GET"])
def pedidos(id):
    cursor = db.get_db_cursor()

    # Solo se van a listar los pedidos que realice el cliente en el día actual
    cursor.execute(
        """
        SELECT * FROM pedido_incluye_reparte WHERE id_pedido IN (
            SELECT numero_pedido FROM factura WHERE id_cliente = %s
            AND fecha = CURRENT_DATE)
        """, (id,)
    )

    pedidos = cursor.fetchall()

    if not pedidos:
        pedidos = []
            
    else:
        for pedido in pedidos:
            pedido['precio'] = f"{pedido['precio']:.2f}"  

    return render_template("cliente/lista_pedidos.html", pedidos = pedidos, id_cliente = id)


# Ruta para listar las facturas de un cliente
@bp.route("/facturas/<int:id>", methods = ["GET"])
def facturas(id):
    cursor = db.get_db_cursor()

    cursor.execute(
        """
        SELECT id_cliente, numero_pedido, fecha, estado FROM factura 
        NATURAL JOIN pedido_incluye_reparte WHERE id_cliente = %s AND estado != 'Seleccionando'
        GROUP BY id_cliente, numero_pedido, fecha, estado
        """,
        (id,)
    )
    facturas = cursor.fetchall()

    print(f"\n\n\n {facturas} \n\n\n")
            
    for factura in facturas:
        # Obtener precio de cada id_pedido
        cursor.execute(
        """
        SELECT SUM(precio) as precio FROM pedido_incluye_reparte WHERE id_pedido = %s
        """,
        (factura["numero_pedido"],)
        )
        factura["precio"] = cursor.fetchone()["precio"]
        factura['precio'] = f"{factura['precio']:.2f}"    

        if factura['estado'] != 'Pendiente de pago':
            factura['estado'] = 'Pagado'


    return render_template("cliente/lista_facturas.html", facturas = facturas)





