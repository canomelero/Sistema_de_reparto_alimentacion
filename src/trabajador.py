from flask import Blueprint, render_template, request, redirect, url_for
from .. import db

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
    en una fecha específica.
    """
    if request.method == "POST":
        # Recoger la fecha del formulario
        fecha = request.form.get("fecha")

        try:
            # Convertir la fecha a un objeto válido
            fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
        except ValueError:
            flash("El formato de la fecha es inválido. Use el formato AAAA-MM-DD.", "danger")
            return redirect(url_for('trabajador.registro'))

        cursor = get_db_cursor()

        # Consultar el tiempo total trabajado (preparación + entrega) y número de pedidos
        cursor.execute(
            """
            SELECT 
                COALESCE(SUM(tiempo_entrega), 0) AS horas_trabajadas,
                COUNT(id_pedido) AS numero_pedidos
            FROM pedido_incluye_reparte
            WHERE id_trabajador = %s AND DATE(fecha) = %s
            """,
            (id_trabajador, fecha)
        )
        datos_trabajador = cursor.fetchone()

        if not datos_trabajador or datos_trabajador["numero_pedidos"] == 0:
            flash("No se encontraron datos para la fecha especificada.", "warning")
            return redirect(url_for('trabajador.registro'))

        # Calcular salario (puedes ajustar la fórmula según tu lógica)
        salario = datos_trabajador["horas_trabajadas"] * 10  # Ejemplo: 10 unidades monetarias por hora trabajada

        # Insertar un nuevo informe en la tabla `informe_trabajador`
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
            (id_informe, fecha, fecha, id_trabajador)
        )

        get_db().commit()

        cursor.execute("SELECT nombre FROM trabajador WHERE id_trabajador = %s", (id_trabajador,))
        nombre_trabajador = cursor.fetchone()["nombre"]

        # Pasar los datos al HTML para mostrarlos
        return render_template(
            "trabajador/informe.html",
            id_trabajador=id_trabajador,
            nombre_trabajador=nombre_trabajador,
            fecha=fecha,
            horas_trabajadas=datos_trabajador["horas_trabajadas"],
            numero_pedidos=datos_trabajador["numero_pedidos"],
            salario=salario
        )
    
    


