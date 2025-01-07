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

bp = Blueprint("trabajador", __name__)

# Ruta para listar los trabajadores de la base de datos
@bp.route("/trabajadores", methods=["GET"])
def listar():
    cursor = db.get_db_cursor()
    trabajadores = []

    if cursor:
        cursor.execute("SELECT * FROM trabajador")
        trabajadores = cursor.fetchall()
        cursor.close()

    return render_template("trabajador/trabajador.html", trabajadores=trabajadores)


# Ruta para registrar un trabajador en la base de datos
@bp.route("/registro", methods=["POST"])
def registro():
    email = request.form["email"]
    nombre = request.form["nombre"]
    direccion = request.form["direccion"]
    telefono = request.form["telefono"]

    if email and nombre and direccion and telefono:
        conexion = db.get_db()
        cursor = db.get_db_cursor()

        cursor.execute("""
            INSERT INTO trabajador (email, nombre, direccion, numero_telefono)
            VALUES (%s, %s, %s, %s)""",
            (email, nombre, direccion, telefono)
        )
        conexion.commit()
        cursor.close()

    return redirect(url_for("trabajador.listar"))


# Ruta para dar de baja a un trabajador de la base de datos
@bp.route("/eliminar/<int:id>", methods=["GET"])
def eliminar(id):
    conexion = db.get_db()
    cursor = db.get_db_cursor()

    cursor.execute("DELETE FROM trabajador WHERE id_trabajador = %s", (id,))
    conexion.commit()
    cursor.close()

    return redirect(url_for("trabajador.listar"))


# Ruta para actualizar/modificar un trabajador de la base de datos
@bp.route("/actualizar/<int:id>", methods=["POST"])
def actualizar(id):
    nombre = request.form["nombre"]
    direccion = request.form["direccion"]
    telefono = request.form["telefono"]

    conexion = db.get_db()
    cursor = db.get_db_cursor()

    cursor.execute("""
        UPDATE trabajador SET nombre = %s, direccion = %s, numero_telefono = %s
        WHERE id_trabajador = %s""",
        (nombre, direccion, telefono, id)
    )
    conexion.commit()
    cursor.close()

    return redirect(url_for("trabajador.listar"))


@bp.route('/trabajador/informe/id_trabajador=<int:id_trabajador>', methods=("GET", "POST"))
def crear_informe_trabajador(id_trabajador: int):
    """
    Genera un informe de las horas trabajadas y pedidos realizados por un trabajador
    en un rango de fechas específico.
    """
    if request.method == "GET":
        cursor = get_db_cursor()
        cursor.execute("SELECT nombre FROM trabajador WHERE id_trabajador = %s", (id_trabajador,))
        trabajador = cursor.fetchone()

        if not trabajador:
            flash("Trabajador no encontrado.", "danger")
            return redirect(url_for('trabajador.listar'))

        return render_template("trabajador/informe.html", nombre_trabajador=trabajador["nombre"])

    if request.method == "POST":
        fecha_inicio = request.form.get("fecha_inicio")
        fecha_fin = request.form.get("fecha_fin")

        try:
            # Convertir las fechas a objetos válidos
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
            if fecha_fin < fecha_inicio:
                raise ValueError("La fecha de fin no puede ser anterior a la fecha de inicio.")
        except ValueError as e:
            flash(str(e), "danger")
            return redirect(url_for('trabajador.crear_informe_trabajador', id_trabajador=id_trabajador))

        cursor = get_db_cursor()

        # Consultar el tiempo total trabajado (preparación + entrega) y número de pedidos
        cursor.execute(
            """
            SELECT 
                COALESCE(SUM(p.tiempo_entrega), 0) AS horas_trabajadas,
                COUNT(p.id_pedido) AS numero_pedidos
            FROM pedido_incluye_reparte p
            JOIN factura f ON p.id_pedido = f.numero_pedido
            WHERE p.id_trabajador = %s AND f.fecha BETWEEN %s AND %s
            """,
            (id_trabajador, fecha_inicio, fecha_fin)
        )
        datos_trabajador = cursor.fetchone()

        if not datos_trabajador or datos_trabajador["numero_pedidos"] == 0:
            flash("No se encontraron datos para el rango de fechas especificado.", "warning")
            return redirect(url_for('trabajador.crear_informe_trabajador', id_trabajador=id_trabajador))

        # Calcular salario
        salario = datos_trabajador["horas_trabajadas"] * 10

        # Crear informe
        cursor.execute(
            """
            INSERT INTO informe_trabajador (id_informe, horas_trabajadas, numero_pedidos, salario) 
            VALUES (DEFAULT, %s, %s, %s)
            RETURNING id_informe
            """,
            (datos_trabajador["horas_trabajadas"], datos_trabajador["numero_pedidos"], salario)
        )
        id_informe = cursor.fetchone()["id_informe"]

        # Vincular el informe al trabajador en la tabla `genera`
        cursor.execute(
            """
            INSERT INTO genera (id_informe, fecha_inicio, fecha_fin, id_trabajador)
            VALUES (%s, %s, %s, %s)
            """,
            (id_informe, fecha_inicio, fecha_fin, id_trabajador)
        )
        get_db().commit()

        return render_template(
            "trabajador/informe.html",
            nombre_trabajador=nombre_trabajador,
            informe={
                "horas_trabajadas": datos_trabajador["horas_trabajadas"],
                "numero_pedidos": datos_trabajador["numero_pedidos"],
                "salario": salario
            },
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )


    
    


