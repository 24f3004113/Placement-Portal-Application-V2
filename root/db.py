from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()


class Admin(db.Model):
    aid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Company(db.Model):
    cid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(100))
    location = db.Column(db.String(100))
    approved = db.Column(db.Boolean, default=False)
    blacklisted = db.Column(db.Boolean, default=False)

    jobs = db.relationship("Job", backref="company")

class Student(db.Model):
    sid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    course = db.Column(db.String(100))
    skills = db.Column(db.String(200))
    resume = db.Column(db.String(200))
    blacklisted = db.Column(db.Boolean, default=False)

    applications = db.relationship("Application", backref="student")
