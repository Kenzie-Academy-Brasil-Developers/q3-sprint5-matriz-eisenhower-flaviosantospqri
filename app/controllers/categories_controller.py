from flask import request, jsonify, session
from http import HTTPStatus


from app.configs.database import db
from sqlalchemy.orm.session import Session
from app.exceptions.exc import InvalidDataError

from app.models.categories_model import Categories
from sqlalchemy.exc import IntegrityError

session: Session = db.session


def create_category():

    keys = ['name', 'description']

    try:

        data = request.get_json()

        if list(data.keys()) != keys:
            return {
                'msg': 'category dont have this key'
            }, HTTPStatus.BAD_REQUEST

        category = Categories(**data)

        db.session.add(category)

        db.session.commit()

        return jsonify(category), HTTPStatus.CREATED

    except IntegrityError:
        session.rollback()
        return {'msg': 'category already exists!'}, HTTPStatus.CONFLICT
    except InvalidDataError as e:
        session.rollback()
        return {'msg': str(e)}


def update_category(id):

    try:
        data = request.get_json()

        current_category = session.query(Categories).get(id)

        for key, value in data.items():
            setattr(current_category, key, value)

        session.add(current_category)
        session.commit()

        return jsonify(current_category), HTTPStatus.OK
    except:
        session.rollback()
        return {'msg': 'category not found!'}, HTTPStatus.NOT_FOUND


def delete_category(id):

    try:
        current_category = session.query(Categories).get(id)

        print(current_category)

        session.delete(current_category)

        session.commit()

        return {}, HTTPStatus.NO_CONTENT
    except:
        session.rollback()
        return {'msg': 'Not Found'}, HTTPStatus.NOT_FOUND
