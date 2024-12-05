from flask import Blueprint, render_template, request, redirect, url_for
import psycopg2
from .. import db

# Creación de blueprint para que todas las rutas de /cliente estén agrupadas
bp = Blueprint("trabajador", __name__)


# Ruta para listar los trabajadores de la base de datos
@bp.route("/trabajadores", methods=["GET", "POST"])
def listar():
    cursor = db.get_db_cursor()
    
    # Obtener trabajadores para listar si es necesario
    # trabajadores = None
    
    # if request.method == "GET" and request.args.get("listar"):
    #     cur.execute("SELECT * FROM Trabajador")
    #     trabajadores = cur.fetchall()
    
    # informe = None
    # if request.method == "POST" and request.form.get("correo"):
    #     correo = request.form["correo"]
    #     cur.execute("SELECT * FROM Informe_Trabajador WHERE correo_electronico = %s", (correo,))
    #     informe = cur.fetchone()

    if(cursor != None):
        cursor.execute(
            "SELECT * FROM trabajador"
        )

        trabajadores = cursor.fecthall()
    
    # He quitado el el envío del informe al html
    return render_template("trabajador.html", trabajadores = trabajadores)


# Ruta para registrar un trabajador en la base de datos
@bp.route("/registro", methods=["POST"])
def registro():
    correo = request.form["correo"]
    nombre = request.form["nombre"]
    direccion = request.form["direccion"]
    telefono = request.form["telefono"]

    if correo and nombre and direccion and telefono:
        conexion = db.get_db()
        cursor = db.get_db_cursor()
        
        cursor.execute("""
            INSERT INTO trabajador (correo_electronico, nombre, direccion, numero_telefono)
            VALUES (%s, %s, %s, %s)""", 
            (correo, nombre, direccion, telefono)
        )

        conexion.commit()
        cursor.close()
    
    return redirect(url_for("trabajador.listar"))


# Ruta para dar de baja a un trabajador de la base de datos
@bp.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    conexion = db.get_db()
    cursor = db.get_db_cursor()

    cursor.execute(
        "DELETE FROM trabajador WHERE id_trabajador = %s", 
        (id,)
    )

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

# @bp.route("/trabajadores/listar", methods=["GET"])
# def listar_trabajadores():
#     return redirect(url_for("trabajadores", listar=True))

@bp.route("/contrato", methods=["POST"])
def contrato():
    id = request.form["id_trabajador"]
    cursor = db.get_db_cursor()

    cursor.execute(
        "SELECT * FROM informe_trabajador WHERE id_trabajador = %s", 
        (id,)
    )

    informe = cursor.fetchone()
    cursor.close()
    
    return redirect(url_for("trabajador.listar"))
