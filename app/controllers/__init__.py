from app.models.eisenhowers_model import Eisenhowers
from app.configs.database import db
from sqlalchemy.orm.session import Session
session: Session = db.session


def eisenhower():
    do_it = {'type': 'Do It First'}
    delegate = {'type': 'Delegate It'}
    schedule = {'type': 'Schedule It'}
    del_it = {'type': 'Delete It'}

    data = [do_it, delegate, schedule, del_it]

    for element in data:
        value_element = Eisenhowers(**element)
        session.add(value_element)
        session.commit()
