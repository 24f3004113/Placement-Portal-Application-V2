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

@student.route("/student/profile", methods=["GET"])
def profile():

    if "uid" not in session or session["role"]!="student":
        return jsonify({"message":"Unauthorized"}),401

    student = Student.query.filter_by(user_id=session["uid"]).first()

    return jsonify({
        "sid":student.sid,
        "name":student.name,
        "email":student.user.email,
        "phone":student.phone,
        "course":student.course,
        "cgpa":student.cgpa,
        "graduation_year":student.graduation_year,
        "skills":student.skills,
        "resume":student.resume
    }),200

@student.route("/student/profile/update", methods=["PUT"])
def update_profile():

    if "uid" not in session or session["role"] != "student":
        return jsonify({"message":"Unauthorized"}),401

    student = Student.query.filter_by(user_id=session["uid"]).first()
    data = request.get_json()

    student.user.password = data.get("password", student.user.password)
    student.user.email = data.get("email", student.user.email)

    student.name = data.get("name", student.name)
    student.phone = data.get("phone", student.phone)
    student.course = data.get("course", student.course)
    student.cgpa = data.get("cgpa", student.cgpa)
    student.graduation_year = data.get("graduation_year", student.graduation_year)
    student.skills = data.get("skills", student.skills)
    student.resume = data.get("resume", student.resume)

    db.session.commit()

    return jsonify({"message":"Profile Updated Successfully"}),200


@student.route("/student/drive/<int:did>", methods=["GET"])
def drive_details(did):
    
    drive = Drive.query.get(did)
    
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
    
    application = Application(student_id=student.sid,drive_id=did)
    
    db.session.add(application)
    db.session.commit()
    
    return jsonify({"message":"Applied Successfully"}),201


@student.route("/student/applications", methods=["GET"])
def applications():
    
    if "uid" not in session or session["role"]!="student":
        return jsonify({"message":"Unauthorized"}),401
    
    student = Student.query.filter_by(user_id=session["uid"]).first()
    
    data=[]
    for application in Application.query.filter_by(student_id=student.sid).all():
        data.append({
            "company":application.drive.company.company_name,
            "job_title":application.drive.job_title,
            "application_date":application.application_date,
            "status":application.status,
            "feedback":application.feedback
        })
        
    return jsonify(data),200

@student.route("/student/interviews", methods=["GET"])
def interviews():
    
    if "uid" not in session or session["role"]!="student":
        return jsonify({"message":"Unauthorized"}),401
    
    student = Student.query.filter_by(user_id=session["uid"]).first()
    
    data=[]
    for application in Application.query.filter_by(student_id=student.sid).all():
        if application.interview:
            data.append({
                "company":application.drive.company.company_name,
                "job_title":application.drive.job_title,
                "date":application.interview.interview_date,
                "time":application.interview.interview_time,
                "mode":application.interview.interview_mode,
                "link":application.interview.interview_link,
                "location":application.interview.interview_location,
                "remarks":application.interview.remarks
            })
            
    return jsonify(data),200

@student.route("/student/placements", methods=["GET"])
def placements():

    if "uid" not in session or session["role"]!="student":
        return jsonify({"message":"Unauthorized"}),401

    student = Student.query.filter_by(user_id=session["uid"]).first()

    data=[]
    for placement in Placement.query.filter_by(student_id=student.sid).all():
        data.append({
            "company":placement.company.company_name,
            "position":placement.position,
            "salary":placement.salary,
            "joining_date":placement.joining_date
        })

    return jsonify(data),200

