from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from config import config
from models.ModelUsers import ModelUsers
from models.entities.users import User


app = Flask(__name__)
app.config['MYSQL_USER'] = 'usuario1'
app.config['MYSQL_PASSWORD'] = 'Sistemas1234!'
app.config['MYSQL_DB'] = 'store'
app.config['MYSQL_HOST'] = 'localhost'
mysql = MySQL(app)

try:
    # Verifica si puedes conectar antes de ejecutar la aplicación
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
            logged_user = ModelUsers.login(mysql, user)
            
            if logged_user is not None:
                if logged_user.usertype == 1:
                    return redirect(url_for("admin"))
                else:
                    return redirect(url_for("home"))
            else:
                flash("Acceso rechazado. Verifica tu nombre de usuario y contraseña.")
                return render_template("auth/login.html")
        except Exception as e:
            print("Error al interactuar con la base de datos:", e)
            flash("Ocurrió un error durante el inicio de sesión. Por favor, inténtalo nuevamente.")
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
    app.config.from_object(config['development'])
    app.run(debug=True)
