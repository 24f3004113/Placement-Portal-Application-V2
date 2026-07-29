from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()


class Admin(db.Model):
    aid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
