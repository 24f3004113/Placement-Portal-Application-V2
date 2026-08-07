from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

db = SQLAlchemy()


class User(db.Model):
    
    __tablename__ = "user"
    
    uid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    
    # admin / company / student
    role = db.Column(db.String(20), nullable=False)


class Company(db.Model):
    
    __tablename__ = "company"
    
    cid = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.uid"), unique=True, nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(100))
    location = db.Column(db.String(100))
    hr_contact = db.Column(db.String(100))
    website = db.Column(db.String(200))
    approval_status = db.Column(db.String(20), default="Pending")
    blacklisted = db.Column(db.Boolean, default=False)

    user = db.relationship("User", backref=db.backref("company", uselist=False))
    drives = db.relationship("Drive", backref="company")


class Student(db.Model):
    
    __tablename__ = "student"
    
    sid = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.uid"), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15))
    course = db.Column(db.String(50))
    cgpa = db.Column(db.Float)
    graduation_year = db.Column(db.Integer)
    skills = db.Column(db.String(300))
    resume = db.Column(db.String(200))
    blacklisted = db.Column(db.Boolean, default=False)
    
    user = db.relationship("User", backref=db.backref("student", uselist=False))
    applications = db.relationship("Application", backref="student")


class Drive(db.Model):
    
    __tablename__ = "drive"
    
    did = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.cid"), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    course = db.Column(db.String(50))
    min_cgpa = db.Column(db.Float)
    graduation_year = db.Column(db.Integer)
    salary = db.Column(db.Integer)
    application_deadline = db.Column(db.Date)
    approval_status = db.Column(db.String(20), default="Pending")
    status = db.Column(db.String(20), default="Open")
    
    applications = db.relationship("Application", backref="drive")

class Application(db.Model):
    
    __tablename__ = "application"
    
    aid = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.sid"), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey("drive.did"), nullable=False)
    application_date = db.Column(db.Date, default=date.today)
    status = db.Column(db.String(30), default="Applied")
    feedback = db.Column(db.Text)

class ApplicationHistory(db.Model):
    
    __tablename__ = "application_history"
    
    hid = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey("application.aid"), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    feedback = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    application = db.relationship("Application", backref="history")

class Placement(db.Model):
    
    __tablename__ = "placement"
    
    pid = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.sid"), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("company.cid"), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey("drive.did"), nullable=False)
    position = db.Column(db.String(100))
    salary = db.Column(db.Integer)
    joining_date = db.Column(db.Date)
    
    student = db.relationship("Student", backref="placement")
    company = db.relationship("Company", backref="placement")
    drive = db.relationship("Drive", backref="placement")

class Interview(db.Model):
    
    __tablename__ = "interview"
    
    iid = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey("application.aid"), unique=True, nullable=False)
    interview_date = db.Column(db.Date)
    interview_time = db.Column(db.Time)
    interview_mode = db.Column(db.String(20))
    interview_link = db.Column(db.String(300))
    interview_location = db.Column(db.String(200))
    remarks = db.Column(db.Text)
    
    application = db.relationship("Application",backref=db.backref("interview", uselist=False))


