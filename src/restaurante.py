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
def add_plato_pedido(id_cliente: int, id_plato: int, id_restaurante: int):
    cursor = get_db_cursor()

    # Savepoint aquí

    if request.method == "POST":
        cursor.execute("SELECT precio, tiempo_preparacion FROM plato_oferta WHERE id_plato = %s",
                      (id_plato,))
        resultado = cursor.fetchone()

        cursor.execute("SELECT CURRENT_DATE")
        fecha_actual = cursor.fetchone()
        print(fecha_actual, "\n\n\n")

        # Asociar trigger aquí para enviarlo a pedidos también y así ahorrar código
        cursor.execute(
            """
            UPDATE ventas_diarias
            SET tiempo_preparacion = tiempo_preparacion + %s, 
                total_ingresado = total_ingresado + %s, 
                platos_vendidos = platos_vendidos + 1
            WHERE id_restaurante = %s AND fecha = %s
            """, 
            (resultado["tiempo_preparacion"], resultado["precio"], id_restaurante, 
             fecha_actual["current_date"], id_plato)
        )

        # Si no se ha hecho el update porque no existe el registro
        if cursor.rowcount == 0: 
            # Obtener el id_trabajador que esté libre.


            # Asociar trigger aquí para crear el pedido y así evitar código extra
            cursor.execute(
                """
                INSERT INTO ventas_diarias (id_restaurante, fecha, tiempo_preparacion,
                total_ingresado, platos_vendidos)
                VALUES (%s, %s, %s, %s, %s)
                """, 
                (id_restaurante, fecha_actual["current_date"], resultado["tiempo_preparacion"],
                 resultado["precio"], 1)
            )
            


        # rollback en caso de error o que se cancele el pedido
        
        get_db().commit()
        return Response(status=204)
        