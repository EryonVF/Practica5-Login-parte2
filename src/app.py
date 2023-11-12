from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from config import config
from models.ModelUsers import ModelUsers
from models.entities.users import User

app = Flask(__name__)
mysql = MySQL(app)

# Configuración de la base de datos
app.config.from_object(config['development'])

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

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            user = User(0, request.form['username'], request.form['password'], 0)
            print("Intento de inicio de sesión para el usuario:", user.username)
            
            with app.app_context():
                logged_user = ModelUsers.login(mysql, user)
            
            print("Usuario autenticado:", logged_user)
            
            if logged_user is not None:
                if logged_user.usertype == 1:
                    return redirect(url_for("admin"))
                else:
                    return redirect(url_for("home"))
            else:
                print("Acceso rechazado. Verifica tu nombre de usuario y contraseña.")
                flash("Acceso rechazado. Verifica tu nombre de usuario y contraseña.", 'error')  # 'error' es el tipo de mensaje
                return render_template("auth/login.html")
        except ValueError as ve:
            print("Contraseña incorrecta:", ve)
            flash("Contraseña incorrecta. Verifica tu nombre de usuario y contraseña.", 'error')
            return render_template("auth/login.html")
        except Exception as e:
            print("Error al interactuar con la base de datos:", e)
            flash("Ocurrió un error durante el inicio de sesión. Por favor, inténtalo nuevamente.", 'error')
            return render_template("auth/login.html")
    else:
        return render_template("auth/login.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/home")
def home():
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)
