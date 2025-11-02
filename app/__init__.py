from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        # імпортуємо моделі для створення таблиць
        from . import models
        db.create_all()

        # blueprints / маршрути
        from .routes import bp as main_bp
        app.register_blueprint(main_bp)

        # створити адміністратора, якщо немає користувачів
        if models.User.query.count() == 0:
            admin = models.User(username='admin', email='admin@example.com', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()

    return app
