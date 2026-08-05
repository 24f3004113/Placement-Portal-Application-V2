from flask import Blueprint, jsonify, session, request
from db import db, Company, Drive, Application, Placement

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
