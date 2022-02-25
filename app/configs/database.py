from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import getenv


db = SQLAlchemy()


def init_app(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('URI_DB')

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.db = db

    from app.models.task_model import Task
    from app.models.task_categories_model import task_categories
    from app.models.categories_model import Categories
    from app.models.eisenhowers_model import Eisenhowers

    with app.app_context():
        db.create_all()
