from flask import Blueprint, jsonify, session, request
from db import db, Company, Drive, Application, Interview

company = Blueprint("company", __name__)

@company.route("/company/dashboard", methods=["GET"])
def company_dashboard():
    
    if "uid" not in session or session["role"] != "company":
        return jsonify({"message": "Unauthorized"}), 401
    
    company = Company.query.filter_by(user_id=session["uid"]).first()
    
    if company is None:
        return jsonify({"message": "Company Not Found"}), 404
    
    total_drives = Drive.query.filter_by(company_id=company.cid).count()
    
    total_applications = Application.query.join(Drive).filter(Drive.company_id == company.cid).count()
    
    selected_students = Application.query.join(Drive).filter(
        Drive.company_id == company.cid,
        Application.status == "Selected"
    ).count()
    
    drives = Drive.query.filter_by(company_id=company.cid).all()
    
    data = []
    
    for drive in drives:
        applications = Application.query.filter_by(drive_id=drive.did).count()
        
        data.append({
            "did": drive.did,
            "job_title": drive.job_title,
            "course": drive.course,
            "salary": drive.salary,
            "application_deadline": drive.application_deadline,
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

@company.route("/company/create_drive", methods=["POST"])
def create_drive():
    
    if "uid" not in session or session["role"] != "company":
        return jsonify({"message": "Unauthorized"}), 401
    
    company = Company.query.filter_by(user_id=session["uid"]).first()
    
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
        application_deadline=data.get("application_deadline")
    )
    
    db.session.add(drive)
    db.session.commit()
    
    return jsonify({"message": "Placement Drive Created Successfully."}), 201

@company.route("/company/edit_drive/<int:did>", methods=["PUT"])
def edit_drive(did):
    
    if "uid" not in session or session["role"] != "company":
        return jsonify({"message": "Unauthorized"}), 401
    
    company = Company.query.filter_by(user_id=session["uid"]).first()
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
def drive_applications(did):
    
    if "uid" not in session or session["role"] != "company":
        return jsonify({"message": "Unauthorized"}), 401
    
    company = Company.query.filter_by(user_id=session["uid"]).first()
    
    if company is None:
        return jsonify({"message": "Company Not Found"}), 404
    
    drive = Drive.query.filter_by(did=did,company_id=company.cid).first()
    
    if drive is None:
        return jsonify({"message": "Drive Not Found"}), 404
    
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
def student_profile(aid):
    
    if "uid" not in session or session["role"] != "company":
        return jsonify({"message": "Unauthorized"}), 401
    
    company = Company.query.filter_by(user_id=session["uid"]).first()
    
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
def update_application(aid):
    
    if "uid" not in session or session["role"] != "company":
        return jsonify({"message":"Unauthorized"}),401
    
    company = Company.query.filter_by(user_id=session["uid"]).first()
    
    application = Application.query.get(aid)
    
    if application is None or application.drive.company_id != company.cid:
        return jsonify({"message":"Application Not Found"}),404
    
    application.status = request.get_json().get("status", application.status)
    
    db.session.commit()
    
    return jsonify({"message":"Application Updated Successfully"}),200

@company.route("/company/application/<int:aid>/interview", methods=["POST"])
def schedule_interview(aid):
    
    if "uid" not in session or session["role"] != "company":
        return jsonify({"message":"Unauthorized"}),401
    
    company = Company.query.filter_by(user_id=session["uid"]).first()
    
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