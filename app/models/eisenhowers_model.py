from dataclasses import dataclass
from sqlalchemy import Column, ForeignKey, Integer, String
from app.configs.database import db


@dataclass
class Eisenhowers(db.Model):
    id: Integer
    type: String

    __tablename__ = 'eisenhowers'
    id = Column(Integer, primary_key=True, nullable=False)
    type = Column(String(100))

    tasks = db.relationship('Task', backref='eisenhowers', uselist=False)
