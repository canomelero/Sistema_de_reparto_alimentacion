# Driver para PostgreSQL
import psycopg2 as pg

# Variable de contexto global que está diseñada para almacenar datos 
# específicos de la solicitud activa
from flask import g

from flask import current_app
import click


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
            dbname = 'python_db',
            user = 'usuario',
            password = 'usuario',
            host = 'localhost'
        )

        g.db.autocommit = False

    return g.db


def init_db():
    """
    Elimina las tablas y los datos almacenados, creando de nuevo las tablas.

    Parámetros:
        None
    
    Return:
        None
    """
    conexion = get_db()
    cursor = conexion.cursor()

    with current_app.open_resource("./schemas/cliente.sql") as file:
        cursor.execute(file.read().decode('utf8'))
        cursor.execute('COMMIT;')


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
        g.db.close()


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
