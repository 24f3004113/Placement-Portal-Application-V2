from flask import Blueprint, jsonify, request, session
from sqlalchemy import or_
from datetime import date
from db import db, Student, Company, Drive, Application, Interview, Placement, ApplicationHistory
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt


student = Blueprint("student", __name__)

@student.route("/student/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    
    uid = int(get_jwt_identity())
    role = get_jwt()["role"]
    
    if "uid" not in session or role != "student":
        return jsonify({"message":"Unauthorized"}),401
    
    student = Student.query.filter_by(user_id=uid).first()
    
    available_drives = []
    
    search = request.args.get("search", "")
    
    if search:
        drives = Drive.query.join(Company).filter(
            Drive.approval_status=="Approved",
            Drive.status=="Open",
            or_(
                Company.company_name.contains(search),
                Drive.job_title.contains(search),
                Drive.description.contains(search)
            )
        ).all()
    else:
        drives = Drive.query.filter_by(approval_status="Approved", status="Open").all()
    
    for drive in drives:
        
        if drive.application_deadline >= date.today():
            
            applied = Application.query.filter_by(student_id=student.sid,drive_id=drive.did).first() is not None
            
            available_drives.append({
                "did": drive.did,
                "company": drive.company.company_name,
                "job_title": drive.job_title,
                "salary": drive.salary,
                "application_deadline": drive.application_deadline.strftime("%d %b %Y"),
                "applied": applied
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
@jwt_required()
def profile():
    
    uid = int(get_jwt_identity())
    role = get_jwt()["role"]
    
    if "uid" not in session or role!="student":
        return jsonify({"message":"Unauthorized"}),401
    
    student = Student.query.filter_by(user_id=uid).first()
    
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
@jwt_required()
def update_profile():
    
    uid = int(get_jwt_identity())
    role = get_jwt()["role"]

    if "uid" not in session or role != "student":
        return jsonify({"message":"Unauthorized"}),401
    
    student = Student.query.filter_by(user_id=uid).first()
    data = request.get_json()
    
    student.user.password = data.get("password", student.user.password)
    student.user.email = data.get("email", student.user.email)
    
    student.name = data.get("name", student.name)
    student.phone = data.get("phone", student.phone)
    student.course = data.get("course", student.course)
    student.cgpa = data.get("cgpa", student.cgpa)
    student.graduation_year = data.get("graduation_year", student.graduation_year)
    student.skills = data.get("skills", student.skills)
    resume = request.files.get("resume")

    if resume:
        if not resume.filename.lower().endswith(".pdf"):
            return jsonify({"message":"Only PDF files are allowed."}),400
        
        filename = str(student.sid) + ".pdf"
        resume.save("static/resumes/" + filename)
        student.resume = filename
        
    db.session.commit()
    
    return jsonify({"message":"Profile Updated Successfully"}),200

@student.route("/student/resume", methods=["GET"])
@jwt_required()
def get_resume():
    
    uid = int(get_jwt_identity())
    role = get_jwt()["role"]
    
    if "uid" not in session or role != "student":
        return jsonify({"message":"Unauthorized"}),401
    
    student = Student.query.filter_by(user_id=uid).first()
    
    if student is None:
        return jsonify({"message":"Student Not Found"}),404
    
    if not student.resume:
        return jsonify({"message":"Resume Not Found"}),404
    
    return jsonify({
        "resume": student.resume
    }),200

@student.route("/student/resume/update", methods=["PUT"])
@jwt_required()
def update_resume():
    
    uid = int(get_jwt_identity())
    role = get_jwt()["role"]
    
    if "uid" not in session or role != "student":
        return jsonify({"message":"Unauthorized"}),401
    
    student = Student.query.filter_by(user_id=uid).first()
    
    if student is None:
        return jsonify({"message":"Student Not Found"}),404
    
    resume = request.files.get("resume")
    
    if not resume:
        return jsonify({"message":"Resume is required."}),400
    
    if not resume.filename.lower().endswith(".pdf"):
        return jsonify({
            "message":"Only PDF files are allowed."
        }),400
        
    filename = str(student.sid) + ".pdf"
    
    resume.save("static/resumes/" + filename)
    
    student.resume = filename
    
    db.session.commit()
    
    return jsonify({
        "message":"Resume Updated Successfully"
    }),200
    


@student.route("/student/drive/<int:did>", methods=["GET"])
@jwt_required()
def drive_details(did):
    
    uid = int(get_jwt_identity())
    role = get_jwt()["role"]
    
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

@student.route("/student/drive/<int:did>/apply", methods=["POST"])
@jwt_required()
def apply(did):
    
    uid = int(get_jwt_identity())
    role = get_jwt()["role"]
    
    if "uid" not in session or role!="student":
        return jsonify({"message":"Unauthorized"}),401
    
    student = Student.query.filter_by(user_id=uid).first()
    
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
@jwt_required()
def applications():
    
    uid = int(get_jwt_identity())
    role = get_jwt()["role"]
    
    if "uid" not in session or role!="student":
        return jsonify({"message":"Unauthorized"}),401
    
    student = Student.query.filter_by(user_id=uid).first()
    
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

@student.route("/student/application/<int:aid>/history", methods=["GET"])
@jwt_required()
def application_history(aid):
    
    uid = int(get_jwt_identity())
    role = get_jwt()["role"]
    
    if "uid" not in session or role != "student":
        return jsonify({"message":"Unauthorized"}),401
    
    student = Student.query.filter_by(user_id=uid).first()
    application = Application.query.filter_by(aid=aid, student_id=student.sid).first()
    
    if application is None:
        return jsonify({"message":"Application Not Found"}),404
    
    history = ApplicationHistory.query.filter_by(application_id=aid).order_by(ApplicationHistory.updated_at).all()
    
    data = []
    
    for history in history:
        data.append({
            "status": history.status,
            "feedback": history.feedback,
            "updated_at": history.updated_at
        })
    return jsonify(data),200

@student.route("/student/history", methods=["GET"])
@jwt_required()
def all_application_history():
    
    uid = int(get_jwt_identity())
    role = get_jwt()["role"]
    
    if "uid" not in session or role != "student":
        return jsonify({"message":"Unauthorized"}),401
    
    student = Student.query.filter_by(user_id=uid).first()
    
    applications = Application.query.filter_by(student_id=student.sid).all()
    
    data = []
    
    for application in applications:
        
        history = ApplicationHistory.query.filter_by(application_id=application.aid).order_by(ApplicationHistory.updated_at).all()
        
        for history in history:
            data.append({
                "application_id": application.aid,
                "company": application.drive.company.company_name,
                "job_title": application.drive.job_title,
                "status": history.status,
                "feedback": history.feedback,
                "updated_at": history.updated_at
            })
            
    return jsonify(data),200

@student.route("/student/interviews", methods=["GET"])
@jwt_required()
def interviews():
    
    uid = int(get_jwt_identity())
    role = get_jwt()["role"]
    
    if "uid" not in session or role!="student":
        return jsonify({"message":"Unauthorized"}),401
    
    student = Student.query.filter_by(user_id=uid).first()
    
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
@jwt_required()
def placements():
    
    uid = int(get_jwt_identity())
    role = get_jwt()["role"]

    if "uid" not in session or role!="student":
        return jsonify({"message":"Unauthorized"}),401

    student = Student.query.filter_by(user_id=uid).first()

    data=[]
    for placement in Placement.query.filter_by(student_id=student.sid).all():
        data.append({
            "company":placement.company.company_name,
            "position":placement.position,
            "salary":placement.salary,
            "joining_date":placement.joining_date
        })

    return jsonify(data),200

