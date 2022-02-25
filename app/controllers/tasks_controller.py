from flask import request, jsonify, session
from http import HTTPStatus

import sqlalchemy


from app.configs.database import db
from sqlalchemy.orm.session import Session
from app.exceptions.exc import InvalidDataError, NumberNotValid
from app.models.categories_model import Categories
from app.models.eisenhowers_model import Eisenhowers

from app.models.task_model import Task
from sqlalchemy.exc import IntegrityError

session: Session = db.session


def create_task():
    try:
        data = request.get_json()
        do_it = (
            session.query(Eisenhowers).filter_by(type='Do It First').first()
        )
        delegate_it = (
            session.query(Eisenhowers).filter_by(type='Delegate It').first()
        )
        schedule_it = (
            session.query(Eisenhowers).filter_by(type='Schedule It').first()
        )
        delete_it = (
            session.query(Eisenhowers).filter_by(type='Delete It').first()
        )
        if data['importance'] == 1 and data['urgency'] == 1:
            data['eisenhower_id'] = do_it.id
        elif data['importance'] == 1 and data['urgency'] == 2:
            data['eisenhower_id'] = delegate_it.id
        elif data['importance'] == 2 and data['urgency'] == 1:
            data['eisenhower_id'] = schedule_it.id
        else:
            data['eisenhower_id'] = delete_it.id

        columns = [
            'name',
            'description',
            'duration',
            'importance',
            'urgency',
            'eisenhower_id',
        ]
        valid_data = {item: data[item] for item in data if item in columns}

        task_render = Task(**valid_data)

        name_ativity = session.query(Eisenhowers).get(
            task_render.eisenhower_id
        )

        categories = []
        for cat in data['categories']:
            category = (
                session.query(Categories)
                .filter(Categories.name == cat)
                .first()
            )

            if category == None:
                new_category = Categories(
                    **{'name': cat, 'description': data['description']}
                )
                session.add(new_category)
                session.commit()
                new_category.tasks.append(task_render)
                categories.append({'name': new_category.name})
            else:
                category.tasks.append(task_render)
                categories.append({'name': category.name})

        session.add(task_render)

        session.commit()

        return {
            'id': task_render.id,
            'name': task_render.name,
            'description': task_render.description,
            'classification': name_ativity.type,
            'categories': categories,
        }, HTTPStatus.CREATED

    except sqlalchemy.exc.IntegrityError as e:
        return {'message': 'task already exists'}, HTTPStatus.CONFLICT
    except NumberNotValid as e:
        return {'msg': str(e)}, HTTPStatus.BAD_REQUEST


def update_task(id):
    try:
        data = request.get_json()

        columns = [
            'name',
            'description',
            'duration',
            'importance',
            'urgency',
            'eisenhower_id',
        ]

        valid_data = {item: data[item] for item in data if item in columns}

        current_task = session.query(Task).get(id)

        do_it = (
            session.query(Eisenhowers).filter_by(type='Do It First').first()
        )
        delegate_it = (
            session.query(Eisenhowers).filter_by(type='Delegate It').first()
        )
        schedule_it = (
            session.query(Eisenhowers).filter_by(type='Schedule It').first()
        )
        delete_it = (
            session.query(Eisenhowers).filter_by(type='Delete It').first()
        )

        for key, value in valid_data.items():
            setattr(current_task, key, value)

        if current_task.importance == 1 and current_task.urgency == 1:
            current_task.eisenhower_id = do_it.id

        elif current_task.importance == 1 and current_task.urgency == 2:
            current_task.eisenhower_id = delegate_it.id

        elif current_task.importance == 2 and current_task.urgency == 1:
            current_task.eisenhower_id = schedule_it.id

        else:
            current_task.eisenhower_id = delete_it.id

        session.add(current_task)
        session.commit()

        return {
            'id': current_task.id,
            'name': current_task.name,
            'description': current_task.description,
            'duration': current_task.duration,
            'classification': session.query(Eisenhowers)
            .get(current_task.eisenhower_id)
            .type,
        }, HTTPStatus.OK
    except:
        return {'message': 'not found'}, HTTPStatus.NOT_FOUND


def delete_task(id):
    try:
        current_task = session.query(Task).get(id)

        session.delete(current_task)

        session.commit()

        return {}, HTTPStatus.NO_CONTENT
    except:
        session.rollback()
        return {'msg': 'Not Found'}, HTTPStatus.NOT_FOUND
