from http import HTTPStatus
from flask import jsonify
from app.models.categories_model import Categories
from app.models.eisenhowers_model import Eisenhowers
from app.models.task_model import Task
from app.configs.database import db
from sqlalchemy.orm.session import Session

session: Session = db.session


def get_all():
    all_categories_task = (
        session.query(Categories, Task, Eisenhowers)
        .filter(Task.eisenhower_id == Eisenhowers.id)
        .all()
    )

    result = []

    for categories, tasks, eisenhowers in all_categories_task:
        result.append(
            {
                'id': categories.id,
                'name': categories.name,
                'description': categories.description,
                'tasks': [
                    {
                        'id': tasks.id,
                        'name': tasks.name,
                        'description': tasks.description,
                        'classifiction': eisenhowers.type,
                    }
                ],
            }
        )
    return jsonify(result), HTTPStatus.OK
