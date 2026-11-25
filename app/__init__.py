from flask import Flask
from config import Config
from .extensions import db, migrate, login_manager, csrf


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    if not app.config.get('SECRET_KEY'):
        raise RuntimeError('SECRET_KEY missing. Add it to your .env file.')

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from importlib import import_module

    main_bp = import_module("app.main.routes").main_bp
    app.register_blueprint(main_bp)

    return app