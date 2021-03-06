from dataclasses import dataclass
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from app.configs.database import db
from sqlalchemy.orm import validates
from app.models.task_categories_model import task_categories
from app.exceptions.exc import InvalidDataError


@dataclass
class Categories(db.Model):
    id: Integer
    name: String
    description: String

    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)

    tasks = db.relationship(
        'Task', secondary=task_categories, backref='categories'
    )

    @validates('name', 'description')
    def validade_values(self, key, value):
        if type(value) != str:
            raise InvalidDataError(
                'error: this type not is valid for this place'
            )
        return value
