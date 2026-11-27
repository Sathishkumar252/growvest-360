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
    login_manager.login_message_category = 'warning'

    from . import models  # noqa: F401

    from .main.routes import main_bp
    from .auth.routes import auth_bp
    from .dashboard.routes import dashboard_bp
    from .profile.routes import profile_bp
    from .salary.routes import salary_bp
    from .calculators.routes import calc_bp
    from .calculators.advanced import advanced_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(salary_bp)
    app.register_blueprint(calc_bp)
    app.register_blueprint(advanced_bp)

    return app