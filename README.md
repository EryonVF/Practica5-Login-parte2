# Practica5-Login-parte2
Link de Github: https://github.com/EryonVF/Practica5-Login-parte2

Primero aceptare que me tomo mucho tiempo realizar esta practica ya que me daba muchos errores en las librerias de mysql, una vez pude realizar la conexion no me funcionaban los usuarios apesar de que habia creado varios siempre me daba un error server internal el cual no me dejaba avanzar, tuve que cambiar librerias y importar algunas de otras maneras al final me daba error solo la de mysql pero me permite ejecutar el programa, despues ya modificando el archivo app, modeluser y el login por fin pude acceder con un usuario que cree en la base el cual era eryon y contraseña 123, la conytraseña la tome como el ejemplo que se agrego al pdf,accedi y me dio el mensaje de bienvenida.



# Conexión a la Base de Datos en Flask

En este proyecto se utiliza Flask, Python, junto con MySQL para gestionar la base de datos. voy a explicar un poco cómo realizar la conexión y acceder a la base de datos.

## Configuración de la Base de Datos

Primero, configura la conexión a la base de datos en el archivo de configuración (`config.py`), donde especificarás detalles como el host, el usuario, la contraseña y el nombre de la base de datos.

class DevelopmentConfig:
    DEBUG = True
    MYSQL_HOST = "localhost"
    MYSQL_USER = "usuario1"
    MYSQL_PASSWORD = "Sistemas1234"
    MYSQL_DB = "store"

config = {
    "development": DevelopmentConfig
}

## Inicialización de la Aplicación Flask

En el archivo principal de la aplicación (`app.py`), inicializa la aplicación Flask y configúrala con la información de la base de datos.

from flask import Flask
from flask_mysqldb import MySQL
from config import config

app = Flask(__name__)
mysql = MySQL(app)

# Configuración de la base de datos
app.config.from_object(config['development'])

## Verificación de la Conexión a la Base de Datos

Antes de ejecutar la aplicación, verifica la conexión a la base de datos para asegurarte de que todo esté configurado correctamente.

try:
    # Verifica la conexión a la base de datos antes de ejecutar la aplicación
    with app.app_context():
        db = mysql.connection
        cursor = db.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        print("Conexión a la base de datos establecida correctamente.")
except Exception as e:
    print("Error de conexión a la base de datos:", e)

## Realización del Login

Al realizar el login, es importante manejar las excepciones y mostrar mensajes de error en caso de fallos. A continuación se presenta un ejemplo básico.

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from config import config
from models.ModelUsers import ModelUsers
from models.entities.users import User

app = Flask(__name__)
mysql = MySQL(app)

# Configuración de la base de datos
app.config.from_object(config['development'])

# ... (código adicional)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            user = User(0, request.form['username'], request.form['password'], 0)
            
            with app.app_context():
                logged_user = ModelUsers.login(mysql, user)
            
            if logged_user is not None:
                # ... (manejo de usuarios autenticados)
            else:
                print("Acceso rechazado. Verifica tu nombre de usuario y contraseña.")
                flash("Acceso rechazado. Verifica tu nombre de usuario y contraseña.")
                return render_template("auth/login.html")
        except Exception as e:
            print("Error al interactuar con la base de datos:", e)
            flash("Ocurrió un error durante el inicio de sesión. Por favor, inténtalo nuevamente.")
            return render_template("auth/login.html")
