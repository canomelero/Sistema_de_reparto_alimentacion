from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
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
def eliminar(id):
    cursor = get_db_cursor()
    cursor.execute("DELETE FROM restaurante WHERE id = %s", (id,))
    get_db().commit()
    return redirect(url_for("restaurante.add", eliminado=True))

