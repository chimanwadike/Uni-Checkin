from datetime import timedelta

from flask import Flask, jsonify
import os

from src.blueprints.attendance import attendance
from src.blueprints.lesson_sessions import lesson_sessions
from src.blueprints.timetables import schedules
from src.blueprints.auth import auth
from src.blueprints.semesters import semesters
from src.blueprints.users import user
from src.blueprints.courses import courses
from src.blueprints.venues import venues
from src.blueprints.roles import roles
from src.blueprints.tutor import tutor
from src.constants.http_status_codes import HTTP_500_INTERNAL_SERVER_ERROR
from src.database.database_context import db
from flasgger import Swagger, swag_from
from src.config.swagger import template, swagger_config
from flask_jwt_extended import JWTManager


def create_app(test_config=None):
    app = Flask(__name__,
                instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=True,
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY'),
            JWT_ACCESS_TOKEN_EXPIRES=timedelta(days=30),
            JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=120),
            SWAGGER={'title': 'UBolton API',
                     'uiversion': 3}

        )
    else:
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)
    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(semesters)
    app.register_blueprint(user)
    app.register_blueprint(courses)
    app.register_blueprint(venues)
    app.register_blueprint(roles)
    app.register_blueprint(schedules)
    app.register_blueprint(tutor)
    app.register_blueprint(lesson_sessions)
    app.register_blueprint(attendance)

    Swagger(app, config=swagger_config, template=template)

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(ex):
        return jsonify({'message': 'something went wrong and we are working on it'}), HTTP_500_INTERNAL_SERVER_ERROR

    return app
