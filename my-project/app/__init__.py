# app/__init__.py

# third-party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

# local imports
from config import app_config
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

from jinja2 import Undefined

# db variable initialization
db = SQLAlchemy()

mail = Mail()

login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True, static_folder='C:\\Users\\USER\\Desktop\\employee_management\\my-project\\app\\static', static_url_path='/static')
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    
    
    Bootstrap(app)
    db.init_app(app)

    
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"

    migrate = Migrate(app, db)

    app.config['MAIL_DEFAULT_SENDER'] = 'ceylontealands@gmail.com'
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'ceylontealands@gmail.com'
    app.config['MAIL_PASSWORD'] = 'kxmdhnjzdqcveihf'

    mail.init_app(app)

    app.jinja_env.globals['isinstance'] = isinstance
    app.jinja_env.globals['Undefined'] = Undefined

    from app import models

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .employees import employees as employees_blueprint
    app.register_blueprint(employees_blueprint)

    from .customer import customers as customer_blueprint
    app.register_blueprint(customer_blueprint)

    return app
