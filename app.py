from flask import Flask, render_template
import os   # Para poder manipular rutas de directorios y archivos
import db as db


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
    return render_template('./cliente/cliente.html')

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
    app.run(debug = True, port = 5000)