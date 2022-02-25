from flask import Blueprint, Flask
from app.routes.categories_routes import bp as bp_category
from app.routes.tasks_routes import bp as bp_task
from app.routes.task_categories_routes import bp as bp_task_categories

bp_api = Blueprint('api', __name__, url_prefix='')


def init_app(app: Flask):
    bp_api.register_blueprint(bp_category)
    bp_api.register_blueprint(bp_task)
    bp_api.register_blueprint(bp_task_categories)

    app.register_blueprint(bp_api)
