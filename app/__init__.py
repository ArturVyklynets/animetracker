import os
from flask import Flask
from dotenv import load_dotenv
from .config import Config
from .auth import google_bp
from .routes import main as main_blueprint


load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = app.config['SECRET_KEY']
    app.register_blueprint(google_bp, url_prefix="/login")
    app.register_blueprint(main_blueprint)
    if app.config['DB_ENABLED']:
        with app.app_context():
            from flask_migrate import Migrate
            from .models import db
            migrate = Migrate()
            db.init_app(app)
            migrate.init_app(app, db)
            db.create_all()
    return app
