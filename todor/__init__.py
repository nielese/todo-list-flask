#Configuraciones básicas de nuestro proyecto
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# Creamos una extension de SQLAlchemy fuera de la funcion
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    #configuración del proyecto
    app.config.from_mapping(
        DEBUG = False,
        SECRET_KEY = "devtodo",
        SQLALCHEMY_DATABASE_URI = "sqlite:///todolist.db"
    )
    # Inicializamos la conección a nuestra base de datos 
    db.init_app(app)

    #Registrar Blueprint
    from . import todo
    app.register_blueprint(todo.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    @app.route("/")
    def index():
        return render_template("index.html")
    
    # Migramos todos los modelos a la base de datos 
    with app.app_context():
        db.create_all()
    
    return app