from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask.ext.login import LoginManager
from flask.ext.assets import Environment
from .bundles import css_all
from flask_mail import Mail

mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
assets = Environment()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    assets.init_app(app)
    assets.register('css_all', css_all)
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,
                           url_prefix = '/auth')

    from .api import api_bp
    app.register_blueprint(api_bp,
                          url_prefix = '/api')

    return app
