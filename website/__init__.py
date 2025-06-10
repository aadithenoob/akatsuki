from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth
import os

load_dotenv()

db = SQLAlchemy()
oauth = OAuth()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "wow such secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL', 'sqlite:///database.db')
    
    db.init_app(app)
    oauth.init_app(app)
    
    from website.routes import routes
    from website.auth import auth
    
    app.register_blueprint(routes, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/auth")
    
    from .models import User
    
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    create_database(app)
    return app

def create_database(app):
    if not path.exists(DB_NAME):
        with app.app_context():
            db.create_all()
            print("Created Database!")