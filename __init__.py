from flask import Flask, render_template
import os   # Para poder manipular rutas de directorios y archivos

from . import db  
from .src import cliente 
from .src import trabajador
from .src import restaurante
from .src import pedido


# # Indicación del directorio donde se encuentra el proyecto (...CRUD-Pyton-Flask/src)
template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

# # Unión de src y templates al directorio del proyecto CRUD-Python-Flask
template_dir = os.path.join(os.getcwd(), 'Sistema_de_reparto_alimentacion','templates')
print(template_dir)


# Inicialización de Flask indicando donde se ubican los archivos
# de plantilla (.html) para que se puedan renderizar
app = Flask(__name__, template_folder = template_dir)
#app = Flask(__name__)

# Para poder usar la función flash() y así mostrar errores por la página
app.config['SECRET_KEY'] = 'psswd'

#Inicializar base de datos
db.init_app(app)

# Registro de los blueprint
app.register_blueprint(cliente.bp, url_prefix = "/cliente")
app.register_blueprint(trabajador.bp, url_prefix = "/trabajador")
app.register_blueprint(restaurante.bp, url_prefix = "/restaurante")
app.register_blueprint(pedido.bp, url_prefix = "/pedido")

# @app.route('/')
# def home():
#     return render_template('./base.html')

# Ruta principal de la app
@app.route('/', methods = ["GET"])
def home():
    """
    Listar todos los clientes de la app
    """
    cursor = db.get_db_cursor()

    if(cursor != None):
        cursor.execute(
            "SELECT * FROM cliente"
        )

        clientes = cursor.fetchall()

    return render_template('cliente/cliente.html', clientes = clientes)



# def create_app():
#     """Función de fábrica para crear y configurar la aplicación

#     Returns
#     -------
#     Objeto de flask
#         Instancia de la aplicación de Flask
#     """
#     # Indicación del directorio donde se encuentra el proyecto (...CRUD-Pyton-Flask/src)
#     # template_dir = os.path.abspath(os.path.dirname(__file__))

#     # # Unión de src y templates al directorio del proyecto CRUD-Python-Flask
#     # template_dir = os.path.join(template_dir, 'templates')

#     # # Inicialización de Flask indicando donde se ubican los archivos
#     # # de plantilla (.html) para que se puedan renderizar
#     # app = Flask(__name__, template_folder = template_dir)
#     app = Flask(__name__, instance_relative_config=True)

#     # Configuración de la aplicación
#     app.config.from_mapping(
#         SECRET_KEY="dev",
#         DATABASE=os.path.join(app.instance_path, "./schemas/cliente.sql"),  # Cambia la ruta si usas otro archivo
#     )

#     # Asegura que la carpeta instance existe
#     try:
#         os.makedirs(app.instance_path)
#     except OSError:
#         pass

#     # Registro de las rutas principales
#     @app.route('/')
#     def home():
#         return render_template('index.html')

#     # Registro de los blueprint
#     app.register_blueprint(cliente.bp, url_prefix="/cliente")

#     # Inicializar la base de datos
#     db.init_app(app)

#     return app


if __name__ == "__main__":
    app.run(debug = True)
    



