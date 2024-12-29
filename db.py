# Driver para PostgreSQL
import psycopg2 as pg
import psycopg2.extras as extras

# Variable de contexto global que está diseñada para almacenar datos 
# específicos de la solicitud activa
from flask import g

from flask import current_app
import click
import os

# Configuración de conexión a PostgreSQL - Juandi
# 
# dbname: "trabajadores",
# user: "ddsiUser",
# password: "ddsiPracticas",
# host: "localhost",
# port: 5432
 

# ---------------------------- Funciones --------------------------------------------------
def get_db():
    """
    Conexión a la base de datos. La conexión será única para cada petición y 
    será reusada en caso de que se vuelva a llamar.

    Parámetros:
        None
    
    Return:
        Objeto conexión
    """
    if 'db' not in g:
        g.db = pg.connect(
            # Datos para la conexión a la db
            dbname = 'reparto_db',
            user = 'ddsiuser',
            password = '',
            host = 'localhost'
        )

        g.db.autocommit = False

    return g.db


def get_db_cursor():
    """
    Creación de cursor a partir de una conexión a la base de datos

    Parámetros:
        None
    
    Return:
        Objeto de tipo cursor
    """
    conexion = get_db()
    return conexion.cursor(cursor_factory = extras.RealDictCursor)


def init_db():
    """
    Elimina las tablas y los datos almacenados, creando de nuevo las tablas.

    Parámetros:
        None
    
    Return:
        None
    """
    cursor = get_db_cursor()

    # path = os.getcwd() + "/sql/schemas/cliente.sql"

    # with open(path, "r") as file:
    #     cursor.execute(file.read())
    #     cursor.execute('COMMIT;')
    schemas = ["restaurante.sql", "trabajador.sql", "pedido.sql", "cliente.sql"]

    for schema in schemas:
        print(f"Archivo: {schema}")
        with current_app.open_resource(f"sql/schemas/{schema}") as f:
            cursor.execute(f.read().decode("utf8"))
            cursor.execute("COMMIT;")

    # Cargar todos los archivos que son triggers
    triggers_files = [f for f in os.listdir("Sistema_de_reparto_alimentacion/sql/triggers")]
    
    for t_files in triggers_files:
        print(f"Archivo: {t_files}")
        with current_app.open_resource(f"sql/triggers/{t_files}") as f:
            cursor.execute(f.read().decode("utf8"))
            cursor.execute("COMMIT;")

    


@click.command('init-db')
def init_db_command():
    """
    Si se ejecuta con el comando "init-db", se borran las tablas y se crean de nuevo

    Parámetros:
        None

    Return:
        None    
    """
    init_db()
    click.echo("Base de Datos inicializada")    # Similar a "print()"


def close_db(exc = None):
    """
    Cierre de la conexión a la base de datos.

    Parámetros:
        - exc: si hay un error durante la solicitud, recibe la excepción. 
    
    Return:
        None
    """

    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_app(app):
    """
    Registro de las funciones de la base de datos con la app de Flask. Es llamada por 
    la Application Factory

    Parámetros:
        - app: aplicación de Flask.
    
    Return:
        None
    """
    app.teardown_appcontext(close_db)   # Asocia la función close_db con el evento teardown
    app.cli.add_command(init_db_command)    # Registra un comando personalizado que se ejecuta desde
                                            # la terminal para inicializar la base de datos
