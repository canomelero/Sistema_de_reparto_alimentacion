from flask import Flask, render_template
import os   # Para poder manipular rutas de directorios y archivos
import db as db

from flask import render_template, request, url_for, redirect


# Indicación del directorio donde se encuentra el proyecto (...CRUD-Pyton-Flask/src)
template_dir = os.path.abspath(os.path.dirname(__file__))

# Unión de src y templates al directorio del proyecto CRUD-Python-Flask
template_dir = os.path.join(template_dir, 'templates')

# Inicialización de Flask indicando donde se ubican los archivos
# de plantilla (.html) para que se puedan renderizar
app = Flask(__name__, template_folder = template_dir)


# Rutas de la app
@app.route('/')
def home():
    return render_template('./index.html')

@app.route('/cliente')
def cliente():
    """
    Listar todos los clientes de la app
    """
    cursor = db.get_db_cursor()

    if(cursor != None):
        cursor.execute(
            "SELECT * FROM cliente"
        )

        clientes = cursor.fetchall()

    return render_template('./cliente/cliente.html', clientes = clientes)


@app.route("/registro", methods = ["POST"])
def registro():
    """
    Registro de un nuevo cliente
    """
    nombre = request.form["nombre-cliente"]
    email = request.form["email"]
    direccion = request.form["direccion"]
    telf = request.form["telefono"]

    if not nombre:
        error = "Es obligatorio introducir el nombre"

    if not email:
        error = "Es obligatorio introducir el email"

    if not direccion:
        error = "Es obligatorio introducir la dirección"
    
    if not telf:
        error = "Es obligatorio introducir el teléfono"
    
    if nombre and email and direccion and telf:
        conexion = db.get_db()
        cursor = db.get_db_cursor()

        cursor.execute(
            "INSERT INTO cliente (nombre, email, direccion, telefono) VALUES (%s, %s, %s, %s)",
            (nombre, email, direccion, telf)
        )

        conexion.commit()
        cursor.close()

    return redirect(url_for("cliente"))







@app.route('/restaurante')
def restaurante():
    return render_template('./restaurante/restaurante.html')

@app.route('/trabajador')
def trabajador():
    return render_template('./trabajador/trabajador.html')

@app.route('/pedido')
def pedido():
    return render_template('./pedido/pedido.html')


if __name__ == '__main__':
    # Crea un contexto de aplicación para inicializar la base de datos
    with app.app_context():
        db.init_db()  # ejecuta init_db en el contexto de la app

    app.run(debug = True, port = 5000)