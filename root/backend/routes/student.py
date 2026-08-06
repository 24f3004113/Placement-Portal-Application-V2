from flask import Blueprint, jsonify, request, session
from datetime import date
from db import db, Student, Company, Drive, Application, Interview, Placement

student = Blueprint("student", __name__)

@student.route("/student/dashboard", methods=["GET"])
def dashboard():
    
    if "uid" not in session or session["role"] != "student":
        return jsonify({"message":"Unauthorized"}),401
    
    student = Student.query.filter_by(user_id=session["uid"]).first()
    
    available_drives = []
    
    drives = Drive.query.filter_by(approval_status="Approved", status="Open").all()
    
    for drive in drives:
        
        if drive.application_deadline >= date.today():
            
            available_drives.append({
                "did": drive.did,
                "company": drive.company.company_name,
                "job_title": drive.job_title,
                "salary": drive.salary,
                "application_deadline": drive.application_deadline
            })
            
    return jsonify({
        "student": student.name,
        "total_applications": Application.query.filter_by(student_id=student.sid).count(),
        "shortlisted": Application.query.filter_by(student_id=student.sid, status="Shortlisted").count(),
        "interviews": Application.query.join(Interview).filter(Application.student_id==student.sid).count(),
        "placements": Placement.query.filter_by(student_id=student.sid).count(),
        "available_drives": available_drives
    }),200

@student.route("/student/drive/<int:did>", methods=["GET"])
def drive_details(did):
    
    drive=Drive.query.get(did)
    
    if drive is None:
        return jsonify({"message":"Drive Not Found"}),404
    
    return jsonify({
        "company":drive.company.company_name,
        "job_title":drive.job_title,
        "description":drive.description,
        "course":drive.course,
        "min_cgpa":drive.min_cgpa,
        "graduation_year":drive.graduation_year,
        "salary":drive.salary,
        "deadline":drive.application_deadline
    }),200

@student.route("/student/apply/<int:did>", methods=["POST"])
def apply(did):
    
    if "uid" not in session or session["role"]!="student":
        return jsonify({"message":"Unauthorized"}),401
    
    student = Student.query.filter_by(user_id=session["uid"]).first()
    
    drive = Drive.query.get(did)
    
    if drive is None:
        return jsonify({"message":"Drive Not Found"}),404
    
    if drive.approval_status!="Approved" or drive.status!="Open":
        return jsonify({"message":"Applications Closed"}),400
    
    if drive.application_deadline<date.today():
        return jsonify({"message":"Application Deadline Over"}),400
    
    if Application.query.filter_by(student_id=student.sid,drive_id=did).first():
        return jsonify({"message":"Already Applied"}),400
    
    application=Application(student_id=student.sid,drive_id=did)
    
    db.session.add(application)
    db.session.commit()
    
    return jsonify({"message":"Applied Successfully"}),201
