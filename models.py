from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    water = db.Column(db.Boolean, default=False)
    workout = db.Column(db.Boolean, default=False)
    steps = db.Column(db.Boolean, default=False)
    journal = db.Column(db.Boolean, default=False)