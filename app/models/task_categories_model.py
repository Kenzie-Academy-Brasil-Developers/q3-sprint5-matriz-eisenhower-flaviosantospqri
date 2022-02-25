from dataclasses import dataclass
from sqlalchemy import Column, ForeignKey, Integer, String
from app.configs.database import db


task_categories = db.Table(
    'task_categories',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('tasks_id', db.Integer, db.ForeignKey('tasks.id')),
    db.Column('categories_id', db.Integer, db.ForeignKey('categories.id')),
)
