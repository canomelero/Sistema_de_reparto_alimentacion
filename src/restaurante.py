from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import Response
from werkzeug.exceptions import abort

from datetime import datetime

from ..db import get_db, get_db_cursor

bp = Blueprint("restaurante", __name__)

@bp.route("/add", methods=("GET", "POST"))
def add():
    cursor = get_db_cursor()

    if request.method == "POST":
        nombre_restuarante = (request.form["restaurante"] if request.form["restaurante"] 
                              else 'Mesón Paco')
        nombre_duenio = request.form["duenio"] if request.form["duenio"] else 'Paco'
        distancia_reparto = (request.form["distancia_reparto"] if request.form["distancia_reparto"] 
                             else '2')
        especialidad = (request.form["especialidad"] if request.form["especialidad"] 
                        else 'Ninguna')
        horario_apertura = (request.form["horario_apertura"] if request.form["horario_apertura"] 
                            else '09:00')
        horario_cierre = (request.form["horario_cierre"] if request.form["horario_cierre"] 
                          else '21:00')

        cursor.execute(
            """
            INSERT INTO restaurante (restaurante, duenio, distancia_reparto, especialidad,
            horario_apertura, horario_cierre)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (nombre_restuarante, nombre_duenio, distancia_reparto, especialidad, 
            horario_apertura, horario_cierre),
        )

        get_db().commit()
    
    cursor.execute("SELECT * FROM restaurante")
    restaurantes = cursor.fetchall()
    return render_template("restaurante/restaurante.html", restaurantes=restaurantes)


@bp.route('/eliminar/<int:id>', methods=("POST", "GET"))
# Id lo obtiene del parámetro ruta int:id
def eliminar(id: int):
    cursor = get_db_cursor()
    cursor.execute("DELETE FROM plato_oferta WHERE id_restaurante = %s", (id,))
    cursor.execute("DELETE FROM restaurante WHERE id = %s", (id,))
    get_db().commit()
    return redirect(url_for("restaurante.add", eliminado=True))


@bp.route('/editar/<int:id>', methods=("POST", "GET"))
def editar(id: int):
    cursor = get_db_cursor()

    # Obtener los valores que había anteriormente en el restaurante
    cursor.execute("SELECT * FROM restaurante WHERE id = %s", (id,))
    restaurante = cursor.fetchone()

    if request.method == "POST":
        # Obtener los nuevos valores del formulario
        nombre_restaurante = (request.form["restaurante"] if request.form["restaurante"] 
                              else restaurante['restaurante'])
        nombre_duenio = (request.form["duenio"] if request.form["duenio"] 
                         else restaurante['duenio'])
        distancia_reparto = (request.form["distancia_reparto"] if request.form["distancia_reparto"]
                            else restaurante['distancia_reparto'])
        especialidad = (request.form["especialidad"] if request.form["especialidad"] 
                        else restaurante['especialidad'])
        horario_apertura = (request.form["horario_apertura"] if request.form["horario_apertura"] 
                            else restaurante['horario_apertura'])
        horario_cierre = (request.form["horario_cierre"] if request.form["horario_cierre"] 
                          else restaurante['horario_cierre'])

        cursor.execute(
            """
            UPDATE restaurante
            SET restaurante = %s, duenio = %s, distancia_reparto = %s, especialidad = %s,
                horario_apertura = %s, horario_cierre = %s
            WHERE id = %s
            """, 
            (nombre_restaurante, nombre_duenio, distancia_reparto, especialidad, 
            horario_apertura, horario_cierre, id))

        get_db().commit()
        return redirect(url_for('restaurante.add'))



@bp.route('/platos/<int:id_restaurante>', methods=("POST", "GET"))
def aniadir_plato(id_restaurante: int):
    cursor = get_db_cursor()

    if request.method == "POST":
        nombre = request.form["nombre"]
        ingredientes = (request.form["ingredientes"] if request.form["ingredientes"] 
                        else "Carne de vacuno (400g) con queso cheddar y cebolla")
        tiempo_preparacion = (request.form["tiempo_preparacion"] if 
                              request.form["tiempo_preparacion"] else "10")
        precio = request.form["precio"]
        disponibilidad = (request.form["disponibilidad"] if request.form["disponibilidad"]
                          else "true")

        cursor.execute(
            """
            INSERT INTO plato_oferta (id_restaurante, nombre, ingredientes, 
            tiempo_preparacion, precio, disponibilidad) VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (id_restaurante, nombre, ingredientes, tiempo_preparacion, precio, disponibilidad),
        )

        get_db().commit()

    cursor.execute("SELECT * FROM plato_oferta WHERE id_restaurante = %s", (id_restaurante,))
    platos_restaurante = cursor.fetchall()

    cursor.execute("SELECT * FROM restaurante WHERE id = %s", (id_restaurante,))
    restaurante = cursor.fetchone()

    return render_template("restaurante/menu.html", platos_restaurante=platos_restaurante,
                           restaurante=restaurante)


@bp.route('/platos/eliminar/id_plato=<int:id_plato>/id_restaurante=<int:id_restaurante>', 
          methods=("POST", "GET"))
def eliminar_plato(id_plato: int, id_restaurante: int):
    cursor = get_db_cursor()
    cursor.execute("DELETE FROM plato_oferta WHERE id_plato = %s", (id_plato,))
    get_db().commit()
    return redirect(url_for("restaurante.aniadir_plato", id_restaurante=id_restaurante, eliminado=True))


@bp.route('/platos/editar/<int:id_plato>/id_restaurante=<int:id_restaurante>', methods=("GET", "POST"))
def editar_plato(id_plato: int, id_restaurante: int):
    cursor = get_db_cursor()

    cursor.execute("SELECT * FROM plato_oferta WHERE id_plato = %s", (id_plato,))
    plato = cursor.fetchone()

    if not plato:
        return redirect(url_for('restaurante.aniadir_plato', id_restaurante=id_restaurante))

    if request.method == "POST":
        nombre = (request.form["nombre"] if request.form["nombre"] else plato['nombre'])
        ingredientes = (request.form["ingredientes"] if request.form["ingredientes"] 
                        else plato['ingredientes'])
        tiempo_preparacion = (request.form["tiempo_preparacion"] if request.form["tiempo_preparacion"] 
                              else plato['tiempo_preparacion'])
        precio = (request.form["precio"] if request.form["precio"] else plato['precio'])
        disponibilidad = (request.form["disponibilidad"] if request.form["disponibilidad"] 
                          else plato['disponibilidad'])

        cursor.execute("""
            UPDATE plato_oferta
            SET nombre = %s, ingredientes = %s, tiempo_preparacion = %s, precio = %s, 
            disponibilidad = %s WHERE id_plato = %s
        """, (nombre, ingredientes, tiempo_preparacion, precio, disponibilidad, id_plato))

        get_db().commit()
        return redirect(url_for("restaurante.aniadir_plato", id_restaurante=id_restaurante))
    
@bp.route('/informe_restaurante/id_restaurante=<int:id_restaurante>', methods=("GET", "POST"))
def crear_informe_restaurante(id_restaurante: int):
    """
    Genera un informe resumido de las ventas y actividades de un restaurante
    en un rango de fechas especificado por el usuario.
    """
    if request.method == "POST":
        # Recoger los datos del formulario
        fecha_inicio = request.form.get("fecha_inicio")
        fecha_fin = request.form.get("fecha_fin")

        try:
            # Convertir las fechas a objetos válidos
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
        except ValueError:
            flash("El formato de las fechas es inválido. Use el formato AAAA-MM-DD.", "danger")
            return redirect(url_for('restaurante.add'))

        if fecha_inicio > fecha_fin:
            flash("La fecha de inicio no puede ser posterior a la fecha de fin.", "danger")
            return redirect(url_for('restaurante.add'))

        cursor = get_db_cursor()
        # COALESCE recibe un conjunto de argumentos y devuelve el primero que no sea nulo.
        cursor.execute(
            """
            SELECT 
                COALESCE(SUM(total_ingresado), 0) AS total_ingresado,
                COALESCE(SUM(platos_vendidos), 0) AS platos_vendidos,
                COALESCE(SUM(tiempo_preparacion), 0) AS tiempo_preparacion
            FROM ventas_diarias
            WHERE id_restaurante = %s AND fecha BETWEEN %s AND %s
            """,
            (id_restaurante, fecha_inicio, fecha_fin)
        )
        informe = cursor.fetchone()

        if not informe:
            flash("No se encontraron datos para el rango de fechas especificado.", "warning")
            return redirect(url_for('restaurante.add'))
        
        cursor.execute(
            """
            INSERT INTO informe_restaurante (id_restaurante, fecha_inicio, fecha_fin, 
            tiempo_preparacion_pedidos, numero_ventas, total_ingresado) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (id_restaurante, fecha_inicio, fecha_fin, informe["tiempo_preparacion"],
             informe["platos_vendidos"], informe["total_ingresado"])
        )

        get_db().commit()

        cursor.execute("SELECT nombre FROM restaurante WHERE id = %s", (id_restaurante,))
        nombre_restaurante = cursor.fetchone()["nombre"]

        # Pasar los datos al HTML para mostrarlos
        return render_template(
            "restaurante/informe_restaurante.html",
            id_restaurante=id_restaurante,
            nombre_restaurante = nombre_restaurante,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            total_ingresado=informe["total_ingresado"],
            platos_vendidos=informe["platos_vendidos"],
            tiempo_preparacion=informe["tiempo_preparacion"]
        )


# ------------------------------------------------------------------
# ------------------------------------------------------------------
#
# A PARTIR DE AQUÍ ES EL CÓDIGO PARA AÑADIR PLATOS A PEDIDOS, ASOCIAR
# CLIENTE A PEDIDO, TRABAJADOR, ETC.
#
# ------------------------------------------------------------------
# ------------------------------------------------------------------

@bp.route('/mostrar_platos/<int:id_cliente>', methods=("GET", "POST"))
def mostrar_rest_plat(id_cliente: int):
    cursor = get_db_cursor()

    cursor.execute("SELECT * FROM restaurante")
    restaurantes = cursor.fetchall()
    
    restaurantes_con_platos = []

    for restaurante in restaurantes:
        cursor.execute(
            "SELECT * FROM plato_oferta WHERE id_restaurante = %s", 
            (restaurante['id'],)
        )

        platos = cursor.fetchall()
        restaurantes_con_platos.append({
            "restaurante": restaurante,
            "platos": platos
        })

    return render_template(
        "restaurante/restaurante_pedidos.html", 
        restaurantes_con_platos=restaurantes_con_platos, 
        id_cliente=id_cliente
    )


@bp.route("/anidadir_plato_pedido/id_cliente=<int:id_cliente>/id_plato=<int:id_plato>"
          "/id_restaurante=<int:id_restaurante>", methods=("GET", "POST"))
def aniadir_plato_pedido(id_cliente: int, id_plato: int, id_restaurante: int):
    cursor = get_db_cursor()

    if request.method != "POST":
        return Response(status=405) # Operacion no permitida
    
    # Comprobar si el cliente tiene un pedido activo en 'Seleccionando'
    cursor.execute(
        """
        SELECT id_pedido FROM pedido_incluye_reparte 
        WHERE estado = 'Seleccionando' AND id_pedido IN 
        (SELECT numero_pedido FROM factura WHERE id_cliente = %s)
        """, (id_cliente,)
    )
    id_pedido_seleccionando = cursor.fetchone()

    # Si no existe un pedido activo, lo creamos
    if not id_pedido_seleccionando:
       resultado = nuevos_registros_pedido_platos(cursor, obtener_fecha_actual(), id_cliente)
       if resultado:
           flash(resultado[0], resultado[1])
           return redirect(url_for('restaurante.mostrar_rest_plat', id_cliente=id_cliente))


    resultado = aniadir_valores_pedido_plato(cursor, id_cliente, id_plato, id_restaurante)
    if resultado:
        flash(resultado[0], resultado[1])
        return redirect(url_for('restaurante.mostrar_rest_plat', id_cliente=id_cliente))
    
    get_db().commit()
    # 204 indica que ha ido todo correcto pero no devuelve ningún recurso
    return Response(status=204) 


@bp.route('/pagar_pedido/<int:id_cliente>', methods=("GET", "POST"))
def finalizar_pedido(id_cliente: int):
    cursor = get_db_cursor()

    # Obtener el id del pedido en estado 'Seleccionando'
    cursor.execute(
        """
        SELECT id_pedido FROM pedido_incluye_reparte 
        WHERE estado = 'Seleccionando' AND id_pedido IN 
        (SELECT numero_pedido FROM factura WHERE id_cliente = %s);
        """, (id_cliente,)
    )
    id_pedido_seleccionando = cursor.fetchone()

    if id_pedido_seleccionando:
        id_pedido = id_pedido_seleccionando["id_pedido"]

        # Calcular el precio total y el tiempo de preparación
        cursor.execute(
            """
            SELECT p.precio, p.tiempo_preparacion
            FROM plato_oferta p
            JOIN pedido_plato pp ON p.id_plato = pp.id_plato
            WHERE pp.id_pedido = %s;
            """, (id_pedido,)
        )
        platos = cursor.fetchall()

        precio_total = sum([plato["precio"] for plato in platos])
        tiempo_preparacion_total = sum([plato["tiempo_preparacion"] for plato in platos])

        # Obtener el id_restaurante del pedido a través de plato_oferta
        cursor.execute(
            """
            SELECT p.id_restaurante
            FROM plato_oferta p
            JOIN pedido_plato pp ON p.id_plato = pp.id_plato
            WHERE pp.id_pedido = %s
            LIMIT 1;
            """, (id_pedido,)
        )
        id_restaurante_data = cursor.fetchone()
        id_restaurante = (id_restaurante_data["id_restaurante"] if id_restaurante_data 
                          else None)

        if not id_restaurante:
            print("No se pudo obtener el id_restaurante.")
            return Response(status=400)

        # Calcular el número de pedidos en estado 'Preparando' en el restaurante
        cursor.execute(
            """
            SELECT COUNT(*) as pedidos_en_preparacion
            FROM pedido_incluye_reparte pir
            WHERE pir.estado = 'Preparando' AND pir.id_pedido IN 
            (SELECT numero_pedido FROM factura WHERE id_cliente = %s);
            """, (id_cliente,)
        )
        pedidos_en_preparacion_data = cursor.fetchone()

        tiempo_entrega_total = 5 + 5 * pedidos_en_preparacion_data["pedidos_en_preparacion"]
        fecha_actual = obtener_fecha_actual()

        resultados = (tiempo_preparacion_total, precio_total, fecha_actual)
        pasar_datos_ventas_diarias(cursor, resultados, id_restaurante, len(platos))

        # Actualizar los valores del pedido en 'pedido_incluye_reparte'
        cursor.execute(
            """
            UPDATE pedido_incluye_reparte
            SET 
                precio = %s,
                tiempo_preparacion = %s,
                tiempo_entrega = %s,
                estado = 'Pendiente de pago'
            WHERE id_pedido = %s;
            """, 
            (precio_total, tiempo_preparacion_total, tiempo_entrega_total, id_pedido)
        )

        # Eliminar los platos del pedido
        cursor.execute("DELETE FROM pedido_plato WHERE id_pedido = %s;", (id_pedido,))

        # Confirmar los cambios
        get_db().commit()
        
    
        return render_template('pedido/pago_pedido.html', 
                               precio_total=precio_total, 
                               tiempo_preparacion_total=tiempo_preparacion_total, 
                               tiempo_entrega_total=tiempo_entrega_total,
                               id_cliente=id_cliente)
    
    return Response(status=500)




@bp.route('/cancelar_pedido/<int:id_cliente>', methods=("GET", "POST"))
def pedido_cancelado(id_cliente: int):
    if request.method == "POST":
        cursor = get_db_cursor()

        cursor.execute(
            """
            SELECT id_pedido, id_trabajador FROM pedido_incluye_reparte 
            WHERE estado = 'Seleccionando' AND id_pedido IN 
            (SELECT numero_pedido FROM factura WHERE id_cliente = %s);
            """, (id_cliente,)
        )
        id_pedido_seleccionando = cursor.fetchone()

        # Comprobar que existe el id_pedido seleccionado
        if id_pedido_seleccionando:
            id_pedido = id_pedido_seleccionando["id_pedido"]

            cursor.execute("DELETE FROM pedido_plato WHERE id_pedido = %s;", (id_pedido,))
            cursor.execute("DELETE FROM factura where numero_pedido = %s;", (id_pedido,))
            cursor.execute("DELETE FROM pedido_incluye_reparte WHERE id_pedido = %s;", 
                           (id_pedido,))
            # Desvincular al trabajador del pedido
            cursor.execute("UPDATE trabajador SET disponibilidad = true WHERE id_trabajador = %s",
                           (id_pedido_seleccionando["id_trabajador"],))
            
            get_db().commit()

        return Response(status=204)
    

def obtener_datos_plato_pedido(cursor, id_plato: int) -> tuple:
    """Obtiene los datos necesarios para añadir plato a pedido y ventas_diarias

    Parameters
    ----------
    cursor : psycopg2.connection.cursor
        Cursor para ejecutar sentencia base de datos
    id_plato : int
        id del plato seleccionado

    Returns
    -------
    list
        Valores necesarios para la consulta insert y update. Valores devueltos son:
        [tiempo_preparacion, precio, fecha actual].
    """
    cursor.execute("SELECT precio, tiempo_preparacion FROM plato_oferta WHERE id_plato = %s",
                    (id_plato,))
    resultado = cursor.fetchone()

    fecha_actual = obtener_fecha_actual()

    return [resultado["tiempo_preparacion"], resultado["precio"], fecha_actual]


def pasar_datos_ventas_diarias(cursor, resultados: tuple, id_restaurante: int,
                               platos_vendidos: int) -> None:
    """Crea o actualiza los valores de ventas_diarias para luego crear informe de restaurante

     Parameters
    ----------
    cursor : psycopg2.connection.cursor
        Cursor para ejecutar sentencia base de datos
    resultados : tuple
        Valores [tiempo_preparacion, precio, fecha actual].
    id_restaurante: int
        ID del restaurante del plato seleccionado

    Returns
    -------
    None
    """
    cursor.execute(
        """
        SELECT 1 FROM ventas_diarias 
        WHERE id_restaurante = %s AND fecha = %s
        """, 
        (id_restaurante, resultados[2])
    )
    ventas_existentes = cursor.fetchone()

    # Comprobar si no existe la tupla de ventas diarias para crearla
    if not ventas_existentes:
        cursor.execute(
            """
            INSERT INTO ventas_diarias (id_restaurante, fecha, tiempo_preparacion, 
            total_ingresado, platos_vendidos) VALUES (%s, %s, %s, %s, %s)
            """, 
            (id_restaurante, resultados[2], resultados[0], resultados[1], platos_vendidos)
        )
        print("Creado ventas_diarias\n\n\n")
    else:
        cursor.execute(
            """
            UPDATE ventas_diarias
            SET tiempo_preparacion = tiempo_preparacion + %s, 
                total_ingresado = total_ingresado + %s, 
                platos_vendidos = platos_vendidos + %s
            WHERE id_restaurante = %s AND fecha = %s
            """, 
            (resultados[0], resultados[1], platos_vendidos, id_restaurante, resultados[2])
        )



def nuevos_registros_pedido_platos(cursor, fecha: str, id_cliente: int) -> tuple | None:
    # Obtener el id_trabajador que esté libre.
    cursor.execute("SELECT id_trabajador FROM trabajador WHERE disponibilidad = true")
    resultado = cursor.fetchone()

    if not resultado:
        print("Ejecutando flash\n\n\n")
        msj = "No se ha encontrado ningún trabajador disponible, vuelva a intentarlo más tarde",
        tipo_error = "danger"
        return (msj, tipo_error)
    
    id_trabajador = resultado["id_trabajador"]
    # Indicar que el repartidor está ocupado ya que se asociará a este envío
    cursor.execute("UPDATE trabajador SET disponibilidad = False WHERE id_trabajador = %s",
                   (id_trabajador,))

    # Para que quede mejor mostrar este error en el html
     
    
    print("Seleccionado trabajador correctamente\n\n\n")
    # crear pedido_incluye_reparte
    cursor.execute(
        """
        INSERT INTO pedido_incluye_reparte (id_trabajador, estado) 
        VALUES (%s, 'Seleccionando') RETURNING id_pedido
        """, (id_trabajador,)
    )
    id_pedido = cursor.fetchone()["id_pedido"] # Obtener el id_pedido de la tupla creada
    print("Creado pedido_incluye_reparte correctamente\n\n\n")

    # Crear tabla factura. Hacer trigger para comprobar que no ha realizado más de 
    # 5 pedidos en un mismo día
    cursor.execute("INSERT INTO factura VALUES (%s, %s, %s)", 
                   (id_pedido, fecha, id_cliente))
    print("Creado factura\n\n\n")


def aniadir_valores_pedido_plato(cursor, id_cliente: int, id_plato: int, id_restaurante: int
                                 ) -> tuple | None:
    """ Añadir nueva tupla a la tabla pedido_plato

    """
    cursor.execute(
        """
        SELECT numero_pedido FROM factura f
        JOIN pedido_incluye_reparte p ON f.numero_pedido = p.id_pedido
        WHERE p.estado = 'Seleccionando' AND id_cliente = %s
        """, (id_cliente,)
    )
    id_pedido = cursor.fetchone()["numero_pedido"]

    # Obtener el id_restaurante del pedido si ya tiene platos
    cursor.execute(
        """
        SELECT DISTINCT p.id_restaurante 
        FROM plato_oferta p
        JOIN pedido_plato pp ON p.id_plato = pp.id_plato
        WHERE pp.id_pedido = %s
        """, (id_pedido,)
    )
    restaurante_existente = cursor.fetchone()

    if restaurante_existente:
        id_restaurante_actual = restaurante_existente["id_restaurante"]

        # Comprobar que el nuevo plato pertenece al mismo restaurante
        if id_restaurante_actual != id_restaurante:
            msj = "Todos los platos en un pedido deben ser del mismo restaurante."
            tipo_error = "error"
            return (msj, tipo_error)
        
    cursor.execute("INSERT INTO pedido_plato VALUES (%s, %s)", (id_pedido, id_plato))


def obtener_fecha_actual()-> str:
    cursor = get_db_cursor()
    cursor.execute("SELECT CURRENT_DATE;")
    return cursor.fetchone()["current_date"]

    