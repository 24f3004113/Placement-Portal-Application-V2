from flask import Blueprint, jsonify, session, request
from db import db, User, Student, Company, Drive, Application, Interview, ApplicationHistory
from sqlalchemy import or_
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime

company = Blueprint("company", __name__)

@company.route("/company/dashboard", methods=["GET"])
@jwt_required()
def company_dashboard():
    
    uid = int(get_jwt_identity())
    role = get_jwt()["role"]
    
    if "uid" not in session or role != "company":
        return jsonify({"message": "Unauthorized"}), 401
    
    company = Company.query.filter_by(user_id=uid).first()
    
    if company is None:
        return jsonify({"message": "Company Not Found"}), 404
    
    total_drives = Drive.query.filter_by(company_id=company.cid).count()
    
    total_applications = Application.query.join(Drive).filter(Drive.company_id == company.cid).count()
    
    selected_students = Application.query.join(Drive).filter(
        Drive.company_id == company.cid,
        Application.status == "Selected"
    ).count()
    search = request.args.get("search", "")
    
    if search:
        drives = Drive.query.filter_by(company_id=company.cid).filter(
            Drive.job_title.contains(search)
        ).all()
    else:
        drives = Drive.query.filter_by(company_id=company.cid).all()
    
    data = []
    
    for drive in drives:
        applications = Application.query.filter_by(drive_id=drive.did).count()
        
        data.append({
            "did": drive.did,
            "job_title": drive.job_title,
            "course": drive.course,
            "salary": drive.salary,
            "application_deadline": drive.application_deadline.strftime("%d %b %Y"),
            "approval_status": drive.approval_status,
            "status": drive.status,
            "applications": applications
        })
        
    return jsonify({
        "company": {
            "company_name": company.company_name,
        },
        
        "summary": {
            "total_drives": total_drives,
            "total_applications": total_applications,
            "selected_students": selected_students
        },
        
        "drives": data
    }), 200

@company.route("/company/profile", methods=["GET"])
@jwt_required()
def company_profile():
    
    uid = int(get_jwt_identity())
    role = get_jwt()["role"]
    
    if "uid" not in session or role != "company":
        return jsonify({"message":"Unauthorized"}),401
    
    company = Company.query.filter_by(user_id=uid).first()
    if company is None:
        return jsonify({"message":"Company Not Found"}),404
    
    return jsonify({
        "company_name":company.company_name,
        "industry":company.industry,
        "location":company.location,
        "hr_contact":company.hr_contact,
        "website":company.website,
        "approval_status":company.approval_status,
        "blacklisted":company.blacklisted
    }),200

@company.route("/company/profile/update", methods=["PUT"])
@jwt_required()
def update_company_profile():
    
    uid = int(get_jwt_identity())
    role = get_jwt()["role"]
    
    if "uid" not in session or role != "company":
        return jsonify({"message":"Unauthorized"}),401
    
    company = Company.query.filter_by(user_id=uid).first()
    if company is None:
        return jsonify({"message":"Company Not Found"}),404
    
    data = request.get_json()
    
    company.user.password = data.get("password", company.user.password)
    company.user.email = data.get("email", company.user.email)
    
    company.company_name = data.get("company_name", company.company_name)
    company.industry = data.get("industry", company.industry)
    company.location = data.get("location", company.location)
    company.hr_contact = data.get("hr_contact", company.hr_contact)
    company.website = data.get("website", company.website)
    
    db.session.commit()
    return jsonify({"message":"Profile Updated Successfully"}),200

@company.route("/company/create_drive", methods=["POST"])
@jwt_required()
def create_drive():
    
    uid = int(get_jwt_identity())
    role = get_jwt()["role"]
    
    
    if "uid" not in session or role != "company":
        return jsonify({"message": "Unauthorized"}), 401
    
    company = Company.query.filter_by(user_id=uid).first()
    
    if company is None:
        return jsonify({"message": "Company Not Found"}), 404
        
    data = request.get_json()
    
    drive = Drive(
        company_id=company.cid,
        job_title=data.get("job_title"),
        description=data.get("description"),
        course=data.get("course"),
        min_cgpa=data.get("min_cgpa"),
        graduation_year=data.get("graduation_year"),
        salary=data.get("salary"),
        application_deadline=datetime.strptime(data.get("application_deadline"),"%Y-%m-%d").date(),
        approval_status="Pending",
        status="Open"
    )
    
    db.session.add(drive)
    db.session.commit()
    
    return jsonify({"message": "Placement Drive Created Successfully."}), 201

@company.route("/company/edit_drive/<int:did>", methods=["PUT"])
@jwt_required()
def edit_drive(did):
    
    uid = int(get_jwt_identity())
    role = get_jwt()["role"]
    
    if "uid" not in session or role != "company":
        return jsonify({"message": "Unauthorized"}), 401
    
    company = Company.query.filter_by(user_id=uid).first()
    drive = Drive.query.filter_by(did=did, company_id=company.cid).first()
    
    if drive is None:
        return jsonify({"message": "Drive Not Found"}), 404
    
    data = request.get_json()
    
    drive.job_title = data.get("job_title", drive.job_title)
    drive.description = data.get("description", drive.description)
    drive.course = data.get("course", drive.course)
    drive.min_cgpa = data.get("min_cgpa", drive.min_cgpa)
    drive.graduation_year = data.get("graduation_year", drive.graduation_year)
    drive.salary = data.get("salary", drive.salary)
    drive.application_deadline = data.get("application_deadline", drive.application_deadline)
    
    db.session.commit()
    
    return jsonify({"message": "Drive Updated Successfully"}), 200

@company.route("/company/drive/<int:did>/applications", methods=["GET"])
@jwt_required()
def drive_applications(did):
    
    uid = int(get_jwt_identity())
    role = get_jwt()["role"]
    
    if "uid" not in session or role != "company":
        return jsonify({"message": "Unauthorized"}), 401
    
    company = Company.query.filter_by(user_id=uid).first()
    
    if company is None:
        return jsonify({"message": "Company Not Found"}), 404
    
    drive = Drive.query.filter_by(did=did,company_id=company.cid).first()
    
    if drive is None:
        return jsonify({"message": "Drive Not Found"}), 404
    search = request.args.get("search", "")

    if search:

        applications = Application.query.filter_by(drive_id=did).join(Student).join(User).filter(
            or_(
                Student.name.contains(search),
                User.email.contains(search),
                Student.course.contains(search)
            )
        ).all()

    else:
        applications = Application.query.filter_by(drive_id=did).all()
    
    data = []
    
    for application in applications:
        
        data.append({
            "aid": application.aid,
            "student_id": application.student.sid,
            "student_name": application.student.name,
            "email": application.student.user.email,
            "phone": application.student.phone,
            "course": application.student.course,
            "cgpa": application.student.cgpa,
            "application_date": application.application_date,
            "status": application.status
        })
        
    return jsonify({
        "company": company.company_name,
        "drive": drive.job_title,
        "applications": data
    }), 200

@company.route("/company/application/<int:aid>/student", methods=["GET"])
@jwt_required()
def student_profile(aid):
    
    uid = int(get_jwt_identity())
    role = get_jwt()["role"]
    
    if "uid" not in session or role != "company":
        return jsonify({"message": "Unauthorized"}), 401
    
    company = Company.query.filter_by(user_id=uid).first()
    
    application = Application.query.get(aid)
    
    if application is None:
        return jsonify({"message": "Application Not Found"}), 404
    
    if application.drive.company_id != company.cid:
        return jsonify({"message": "Unauthorized"}), 401
        
    student = application.student
    
    return jsonify({
        "sid": student.sid,
        "name": student.name,
        "email": student.user.email,
        "phone": student.phone,
        "course": student.course,
        "cgpa": student.cgpa,
        "graduation_year": student.graduation_year,
        "skills": student.skills,
        "resume": student.resume
    }), 200
    
@company.route("/company/application/<int:aid>/update", methods=["PUT"])
@jwt_required()
def update_application(aid):
    
    uid = int(get_jwt_identity())
    role = get_jwt()["role"]
    
    if "uid" not in session or role != "company":
        return jsonify({"message":"Unauthorized"}),401
    
    company = Company.query.filter_by(user_id=uid).first()
    
    application = Application.query.get(aid)
    
    if application is None or application.drive.company_id != company.cid:
        return jsonify({"message":"Application Not Found"}),404
    
    data = request.get_json()
    
    application.status = data.get("status", application.status)
    application.feedback = data.get("feedback", application.feedback)
    
    history = ApplicationHistory(
        application_id = application.aid,
        status = application.status,
        feedback = application.feedback
    )
    
    db.session.add(history)
    
    db.session.commit()
    
    return jsonify({"message":"Application Updated Successfully"}),200

@company.route("/company/application/<int:aid>/history", methods=["GET"])
@jwt_required()
def application_history(aid):
    
    uid = int(get_jwt_identity())
    role = get_jwt()["role"]
    
    if "uid" not in session or role != "company":
        return jsonify({"message":"Unauthorized"}),401
    
    company = Company.query.filter_by(user_id=uid).first()
    application = Application.query.get(aid)
    
    if application is None or application.drive.company_id != company.cid:
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

@company.route("/company/application/<int:aid>/interview", methods=["POST"])
@jwt_required()
def schedule_interview(aid):
    
    uid = int(get_jwt_identity())
    role = get_jwt()["role"]
    
    if "uid" not in session or role != "company":
        return jsonify({"message":"Unauthorized"}),401
    
    company = Company.query.filter_by(user_id=uid).first()
    
    application = Application.query.get(aid)
    
    if application is None or application.drive.company_id != company.cid:
        return jsonify({"message":"Application Not Found"}),404
    
    if application.status != "Shortlisted":
        return jsonify({"message": "Only shortlisted students can be scheduled for interview."}), 400
    
    data = request.get_json()
    
    interview = Interview(
        application_id=aid,
        interview_date=data.get("interview_date"),
        interview_time=data.get("interview_time"),
        interview_mode=data.get("interview_mode"),
        interview_link=data.get("interview_link"),
        interview_location=data.get("interview_location"),
        remarks=data.get("remarks")
    )
    
    db.session.add(interview)
    
    application.status = "Interview"
    
    db.session.commit()
    
    return jsonify({"message":"Interview Scheduled Successfully"}),201

@company.route("/company/interview/<int:iid>/update", methods=["PUT"])
@jwt_required()
def update_interview(iid):
    
    uid = int(get_jwt_identity())
    role = get_jwt()["role"]
    
    if "uid" not in session or role != "company":
        return jsonify({"message":"Unauthorized"}),401
    
    company = Company.query.filter_by(user_id=uid).first()
    
    interview = Interview.query.get(iid)
    
    if interview is None or interview.application.drive.company_id != company.cid:
        return jsonify({"message":"Interview Not Found"}),404
    
    data = request.get_json()
    
    interview.interview_date = data.get("interview_date", interview.interview_date)
    interview.interview_time = data.get("interview_time", interview.interview_time)
    interview.interview_mode = data.get("interview_mode", interview.interview_mode)
    interview.interview_link = data.get("interview_link", interview.interview_link)
    interview.interview_location = data.get("interview_location", interview.interview_location)
    interview.remarks = data.get("remarks", interview.remarks)
    
    db.session.commit()
    
    return jsonify({"message":"Interview Updated Successfully"}),200