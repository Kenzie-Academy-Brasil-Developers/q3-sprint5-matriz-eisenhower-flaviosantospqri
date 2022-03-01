from flask import Flask, Blueprint

from app.controllers import task_categories_controller

bp = Blueprint(
    '',
    __name__,
)

bp.get('/')(task_categories_controller.get_all)
