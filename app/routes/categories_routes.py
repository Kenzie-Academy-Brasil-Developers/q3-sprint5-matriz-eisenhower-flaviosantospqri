from flask import Flask, Blueprint

from app.controllers import categories_controller

bp = Blueprint('categories', __name__, url_prefix='categories')

bp.post('')(categories_controller.create_category)

bp.patch('/<id>')(categories_controller.update_category)

bp.delete('/<id>')(categories_controller.delete_category)
