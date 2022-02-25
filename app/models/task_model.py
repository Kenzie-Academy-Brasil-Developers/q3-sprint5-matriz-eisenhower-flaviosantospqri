from dataclasses import dataclass

from sqlalchemy import Column, Integer, String, ForeignKey, Text
from app.configs.database import db
from sqlalchemy.orm import backref, relationship, validates

from app.exceptions.exc import NumberNotValid
from app.models.eisenhowers_model import Eisenhowers


@dataclass
class Task(db.Model):
    id: int
    name: str
    description: str
    duration: int
    importance: int
    urgency: int
    eisenhower_id: int

    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    duration = Column(Integer)
    importance = Column(Integer)
    urgency = Column(Integer)
    eisenhower_id = Column(
        Integer, ForeignKey('eisenhowers.id'), nullable=False
    )

    @validates('importance', 'urgency')
    def validate_value_range(self, key, value):
        valid_values = [1, 2]
        if value not in valid_values or type(value) != int:
            raise NumberNotValid(value, value)

        return value
