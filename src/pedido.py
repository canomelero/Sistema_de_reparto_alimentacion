from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import Response
from werkzeug.exceptions import abort

from ..db import get_db, get_db_cursor

bp = Blueprint("pedido", __name__)

@bp.route('/pedidos', methods=["GET", "POST"])
def listar_pedidos_filtrados():
    cursor = get_db_cursor()
    pedidos = []

    if request.method == "POST":
        # Obtener los datos del formulario
        tipo_acceso = request.form.get('Tipo_Acceso')
        identificador = request.form.get('Identificador')

        cursor = get_db_cursor()

        # Asegurarse de que los datos del formulario estén presentes
        if not tipo_acceso or not identificador:
            return "Datos incompletos", 400

        # Definir la consulta SQL según el tipo de acceso
        if tipo_acceso == "opcion1":  # Trabajador
            cursor.execute(
                """
                SELECT * FROM pedido_incluye_reparte
                WHERE id_trabajador = %s
                """, (identificador,)
            )
        elif tipo_acceso == "opcion2":  # Restaurante
            cursor.execute(
                """
                SELECT * FROM pedido_incluye_reparte
                WHERE id_restaurante = %s
                """, (identificador,)  # Asegúrate de que esta columna exista
            )
        elif tipo_acceso == "opcion3":  # Cliente
            cursor.execute(
                """
                SELECT * FROM pedido_incluye_reparte WHERE id_pedido IN (
                SELECT numero_pedido FROM factura WHERE id_cliente = %s)
                """, (identificador,)
            )
        else:
            return "Tipo de acceso inválido", 400

        # Obtener los pedidos filtrados
        pedidos = cursor.fetchall()


    # Renderizar la plantilla con los pedidos filtrados
    return render_template('pedido/pedido.html',
                           mostrar_encabezado=True, 
                           pedido_incluye_reparte=pedidos)


@bp.route('/pedidos/todos', methods = ["GET"])
def listarPedidos():
    cursor = get_db_cursor()

    if(cursor != None):
        cursor.execute(
        """
        SELECT * FROM pedido_incluye_reparte;
        """
    )

        
        pedidos = cursor.fetchall()

        if not pedidos:
            pedidos = []

        else:
            for pedido in pedidos:
                pedido['precio'] = f"{pedido['precio']:.2f}"  

    return render_template('pedido/pedido.html',
                            mostrar_encabezado=False,
                            pedido_incluye_reparte = pedidos)


@bp.route('/pedido/datos_restantes?<int:id_pedido>&<int:id_cliente>', methods=["POST"])
def datos_restantes(id_pedido, id_cliente):
    db = get_db()
    cursor = get_db_cursor()

    # Obtener datos del formulario
    direccion_entrega = request.form.get("direccion")
    observaciones = request.form.get("observaciones")

    # Validar datos
    if not direccion_entrega or not observaciones:
        return "Datos inválidos", 400

    try:
        # Ejecutar el UPDATE en la base de datos
        cursor.execute(
            """
            UPDATE pedido_incluye_reparte 
            SET direccion_entrega = %s, observaciones = %s, estado = %s
            WHERE id_pedido = %s;
            """,
            (direccion_entrega, observaciones, "Preparando",  id_pedido)
        )

        db.commit()

        # Verificar si se actualizó algo
        if cursor.rowcount == 0:
            return f"No se encontró el pedido con ID {id_pedido}", 404

    except Exception as e:
        db.rollback()
        return f"Error al actualizar el pedido: {str(e)}", 500

    # Redirigir a una página de éxito o mostrar el mismo modal actualizado
    return redirect(url_for("cliente.pedidos", id=id_cliente))


