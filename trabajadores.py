from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# Configuración de conexión a PostgreSQL
DB_CONFIG = {
    "dbname": "trabajadores",
    "user": "ddsiUser",
    "password": "ddsiPracticas",
    "host": "localhost",
    "port": 5432,
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/trabajadores", methods=["GET", "POST"])
def trabajadores():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    # Obtener trabajadores para listar si es necesario
    trabajadores = None
    if request.method == "GET" and request.args.get("listar"):
        cur.execute("SELECT * FROM Trabajador")
        trabajadores = cur.fetchall()
    
    informe = None
    if request.method == "POST" and request.form.get("correo"):
        correo = request.form["correo"]
        cur.execute("SELECT * FROM Informe_Trabajador WHERE correo_electronico = %s", (correo,))
        informe = cur.fetchone()
    
    cur.close()
    conn.close()
    return render_template("trabajadores.html", trabajadores=trabajadores, informe=informe)

@app.route("/trabajadores/alta", methods=["POST"])
def alta_trabajador():
    correo = request.form["correo"]
    nombre = request.form["nombre"]
    direccion = request.form["direccion"]
    telefono = request.form["telefono"]

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Trabajador (correo_electronico, nombre, direccion, numero_telefono)
        VALUES (%s, %s, %s, %s)
    """, (correo, nombre, direccion, telefono))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("trabajadores"))

@app.route("/trabajadores/baja", methods=["POST"])
def baja_trabajador():
    correo = request.form["correo"]

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("DELETE FROM Trabajador WHERE correo_electronico = %s", (correo,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("trabajadores"))

@app.route("/trabajadores/modificar", methods=["POST"])
def modificar_trabajador():
    correo = request.form["correo"]
    nuevo_nombre = request.form["nombre"]
    nueva_direccion = request.form["direccion"]
    nuevo_telefono = request.form["telefono"]

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        UPDATE Trabajador
        SET nombre = %s, direccion = %s, numero_telefono = %s
        WHERE correo_electronico = %s
    """, (nuevo_nombre, nueva_direccion, nuevo_telefono, correo))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("trabajadores"))

@app.route("/trabajadores/listar", methods=["GET"])
def listar_trabajadores():
    return redirect(url_for("trabajadores", listar=True))

@app.route("/trabajadores/consultar", methods=["POST"])
def consultar_contrato():
    correo = request.form["correo"]

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Informe_Trabajador WHERE correo_electronico = %s", (correo,))
    informe = cur.fetchone()
    cur.close()
    conn.close()
    return redirect(url_for("trabajadores"))

if __name__ == "__main__":
    app.run(debug=True)
