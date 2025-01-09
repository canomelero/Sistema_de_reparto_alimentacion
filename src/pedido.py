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
        identificador = (request.form.get('Identificador') if request.form.get("Identificador") 
                         else 0)
        cursor = get_db_cursor()

        # Trabajador
        if tipo_acceso == "opcion1":  
            cursor.execute(
                """
                SELECT * FROM pedido_incluye_reparte
                WHERE id_trabajador = %s
                """, (identificador,)
            )
        # Cliente
        elif tipo_acceso == "opcion2":  
            cursor.execute(
                """
                SELECT * FROM pedido_incluye_reparte WHERE id_pedido IN (
                SELECT numero_pedido FROM factura WHERE id_cliente = %s)
                """, (identificador,)
            )
        else:
            return redirect(url_for("pedido.listar_pedidos"))

        # Obtener los pedidos filtrados
        pedidos = cursor.fetchall()

        for pedido in pedidos:
            cursor.execute(
                """
                SELECT COUNT(*) AS num_platos FROM pedido_plato WHERE id_pedido = %s;
                """,
                (pedido["id_pedido"],)
            )
            pedido["numero_platos"] = cursor.fetchone()["num_platos"]


    # Renderizar la plantilla con los pedidos filtrados
    return render_template('pedido/pedido.html',
                           mostrar_encabezado=True, 
                           pedido_incluye_reparte=pedidos)


@bp.route('/pedidos/todos', methods = ["GET"])
def listar_pedidos():
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

    for pedido in pedidos:
        cursor.execute(
            """
            SELECT COUNT(*) AS num_platos FROM pedido_plato WHERE id_pedido = %s;
            """,
            (pedido["id_pedido"],)
        )
        pedido["numero_platos"] = cursor.fetchone()["num_platos"]

    return render_template('pedido/pedido.html',
                            mostrar_encabezado=False,
                            pedido_incluye_reparte = pedidos)




@bp.route('/pedido/datos_restantes?<int:id_pedido>', methods=["POST"])
def datos_restantes(id_pedido):
    db = get_db()
    cursor = get_db_cursor()

    # Obtener datos del formulario
    direccion_entrega = request.form.get("direccion")
    observaciones = request.form.get("observaciones")

    # Validar datos
    if not direccion_entrega:
        return "Datos inválidos", 400

    try:
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

    # Redirigir a la página de inicio
    return redirect("/")


@bp.route('/pedido/trabajador?id_pedido=<int:id_pedido>', methods=['GET', 'POST'])
def modificar_pedido_trabajador(id_pedido):
    db = get_db()
    cursor = get_db_cursor()
    estado = request.form['estado'] 

    try:
        posibles_estados = ("En reparto", "Entregado")

        if estado not in posibles_estados:
            raise ValueError("El estado indicado no existe, debe de ser En reparto o Entregado")

        cursor.execute(
            "ALTER TABLE pedido_incluye_reparte DISABLE TRIGGER trg_validar_modificacion_pedido;"
        )

        cursor.execute(
            """
            UPDATE pedido_incluye_reparte 
            SET estado = %s
            WHERE id_pedido = %s;
            """,
            (estado , id_pedido)
        )

        cursor.execute(
            "ALTER TABLE pedido_incluye_reparte ENABLE TRIGGER trg_validar_modificacion_pedido;"
        )
        db.commit()

        # Verificar si se actualizó algo
        if cursor.rowcount == 0:
            return f"No se encontró el pedido con ID {id_pedido}", 404

    except ValueError as e:
        flash(str(e), "danger")
    except Exception as e:
        db.rollback()
        return f"Error al actualizar el pedido: {str(e)}", 500
    finally:
        return redirect(url_for("pedido.listar_pedidos"))


@bp.route('/pedido/cliente?id_pedido=<int:id_pedido>&id_cliente=<int:id_cliente>', methods=['GET','POST'])
def modificar_pedido_cliente(id_pedido, id_cliente):
    db = get_db()
    cursor = get_db_cursor()
    direccion_entrega = request.form.get("direccion")
    observaciones = request.form.get("observaciones")

    if not direccion_entrega:
        return "Datos inválidos", 400

    try:
        cursor.execute(
            """
            UPDATE pedido_incluye_reparte 
            SET direccion_entrega = %s, observaciones = %s
            WHERE id_pedido = %s;
            """,
            (direccion_entrega, observaciones, id_pedido)
        )

        db.commit()

        # Verificar si se actualizó algo
        if cursor.rowcount == 0:
            return f"No se encontró el pedido con ID {id_pedido}", 404

    except Exception as e:
        db.rollback()
        return f"Error al actualizar el pedido: {str(e)}", 500

    return redirect(url_for("cliente.pedidos", id = id_cliente))