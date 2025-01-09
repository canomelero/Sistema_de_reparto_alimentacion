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
    return render_template('pedido/pedido.html', pedido_incluye_reparte=pedidos)


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

    return render_template('pedido/tabla_pedidos_restaurante.html', pedido_incluye_reparte = pedidos)




<<<<<<< Updated upstream
@bp.route('/pedido/datos_restantes/<int:id_pedido>', methods=["POST"])
def datos_restantes(id_pedido):
=======
@bp.route('/pedido/datos_restantes?<int:id_pedido>&<int:id_cliente>', methods=['GET',"POST"])
def datos_restantes(id_pedido, id_cliente):
>>>>>>> Stashed changes
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
            (direccion_entrega, observaciones, "Pagado",  id_pedido)
        )
        db.commit()

        # Verificar si se actualizó algo
        if cursor.rowcount == 0:
            return f"No se encontró el pedido con ID {id_pedido}", 404

    except Exception as e:
        db.rollback()
        return f"Error al actualizar el pedido: {str(e)}", 500

    # Redirigir a una página de éxito o mostrar el mismo modal actualizado
<<<<<<< Updated upstream
    return redirect(url_for("pedido.listarPedidos"))
=======
    return redirect(url_for("cliente.pedidos", id=id_cliente))


@bp.route('/pedido/modificar/<int:id_pedido>', methods=['GET', 'POST'])
def modificar_pedido(id_pedido):
    # Obtener el tipo de acceso desde los parámetros
    #identificador = request.form["identificador"]
    #tipo_acceso = request.form["tipo_acceso"]
    #print(f"\n\n\n{tipo_acceso}     \n\n\n")
    cursor = get_db_cursor()


    cursor.execute("SELECT id_cliente FROM factura WHERE numero_pedido=%s;", (id_pedido,))
    id_cliente = cursor.fetchone()
    
    # Mostrar formulario para Trabajador o Cliente
    #if tipo_acceso == "opcion1": #trabajador
    #    return render_template('pedido/modificar_trabajador.html', id_pedido=id_pedido)
    #elif tipo_acceso == "opcion3": #cliente
    <a href="{{ url_for('pedido.modificar_pedido_cliente', id_pedido=id_pedido, id_cliente=id_cliente) }}" class="btn btn-primary">
    Modificar Pedido
</a>
    #else:   
     #   return "Tipo de acceso no válido", 400
        #return redirect(url_for("pedido.listar_pedidos_filtrados"))



@bp.route('/pedido/trabajador?id_pedido=<int:id_pedido>', methods=['GET', 'POST'])
def modificar_pedido_trabajador(id_pedido):
    db = get_db()
    cursor = get_db_cursor()
    estado = request.args.get('estado') 

    try:
        # Ejecutar el UPDATE en la base de datos
        cursor.execute(
            """
            UPDATE pedido_incluye_reparte 
            SET estado = %s
            WHERE id_pedido = %s;
            """,
            (estado , id_pedido)
        )

        db.commit()

        # Verificar si se actualizó algo
        if cursor.rowcount == 0:
            return f"No se encontró el pedido con ID {id_pedido}", 404

    except Exception as e:
        db.rollback()
        return f"Error al actualizar el pedido: {str(e)}", 500
    
    return redirect(url_for("pedido.listar_pedidos_filtrados"))



@bp.route('/pedido/cliente/id_pedido=<int:id_pedido>/id_cliente=<int:id_cliente>', methods=['GET','POST'])
def modificar_pedido_cliente(id_pedido, id_cliente):
    db = get_db()
    cursor = get_db_cursor()
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

    # Redirigir a una página de éxito o mostrar el mismo modal actualizado
    return redirect(url_for("cliente.pedidos", id=id_cliente))
>>>>>>> Stashed changes
