from os import environ
from os.path import dirname

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .key import get_key

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = get_key()
    app.config['SQLALCHEMY_DATABASE_URI'] = environ['SQLALCHEMY_DATABASE_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['BASE_DIR'] = dirname(dirname(__file__))

    __import__("app.models")
    db.init_app(app)
    migrate.init_app(app, db)

    from . import views
    for view in [getattr(views, x) for x in views.__all__]:
        app.register_blueprint(view.bp)

    from . import error
    app.register_error_handler(error.LetsGo, error.lets_go_handler)
    app.register_error_handler(404, error.not_found_handler)
    app.register_error_handler(405, error.not_found_handler)

    from . import tools
    app.add_template_filter(tools.get_user_block)

    return app
