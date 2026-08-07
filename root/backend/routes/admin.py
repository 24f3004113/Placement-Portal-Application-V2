from flask import Blueprint, jsonify, session, request
from sqlalchemy import or_
from db import db, User, Company, Student, Drive, Application ,ApplicationHistory
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

admin = Blueprint("admin", __name__)


@admin.route("/admin/dashboard", methods=["GET"])
@jwt_required()
def admin_dashboard():
    
    uid = int(get_jwt_identity())
    role = get_jwt()["role"]
    
    if role != "admin":
        return jsonify({"message":"Unauthorized"}),401
    
    students = Student.query.count()
    companies = Company.query.count()
    drives = Drive.query.count()
    applications = Application.query.count()
    
    return jsonify({
        "students": students,
        "companies": companies,
        "drives": drives,
        "applications": applications
    }), 200
    

@admin.route("/admin/students", methods=["GET"])
@jwt_required()
def all_students():
    
    uid = int(get_jwt_identity())
    role = get_jwt()["role"]
    
    if role != "admin":
        return jsonify({"message":"Unauthorized"}),401
    
    search = request.args.get("search", "")
    
    if search:
        students = Student.query.join(User).filter(
            or_(
                Student.name.contains(search),
                User.email.contains(search),
                Student.course.contains(search)
            )
        ).all()
    else:
        students = Student.query.all()
        
    data = []
    
    for student in students:
        data.append({
            "sid": student.sid,
            "name": student.name,
            "email": student.user.email,
            "phone": student.phone,
            "course": student.course,
            "cgpa": student.cgpa,
            "graduation_year": student.graduation_year,
            "skills": student.skills,
            "blacklisted": student.blacklisted
        })
        
    return jsonify(data), 200


@admin.route("/admin/companies", methods=["GET"])
@jwt_required()
def all_companies():
    uid = int(get_jwt_identity())
    role = get_jwt()["role"]
    
    if role != "admin":
        return jsonify({"message":"Unauthorized"}),401
    
    search = request.args.get("search", "")
    
    if search:
        companies = Company.query.join(User).filter(
            or_(
                Company.company_name.contains(search),
                User.email.contains(search),
                Company.industry.contains(search)
            )
        ).all()
    else:
        companies = Company.query.all()
    
    data = []
    
    for company in companies:
        data.append({
            "cid": company.cid,
            "company_name": company.company_name,
            "email": company.user.email,
            "industry": company.industry,
            "location": company.location,
            "hr_contact": company.hr_contact,
            "website": company.website,
            "approval_status": company.approval_status,
            "blacklisted": company.blacklisted
        })
        
    return jsonify(data), 200


@admin.route("/admin/company/pending", methods=["GET"])
@jwt_required()
def pending_companies():
    
    uid = int(get_jwt_identity())
    role = get_jwt()["role"]
    
    if role != "admin":
        return jsonify({"message":"Unauthorized"}),401
        
    companies = Company.query.filter_by(approval_status="Pending").all()
    
    data = []
    
    for company in companies:
        data.append({
            "cid": company.cid,
            "company_name": company.company_name,
            "industry": company.industry,
            "location": company.location,
            "hr_contact": company.hr_contact,
            "website": company.website
        })
        
    return jsonify(data), 200


@admin.route("/admin/company/<int:cid>/approve", methods=["PUT"])
@jwt_required()
def approve_company(cid):
    
    uid = int(get_jwt_identity())
    role = get_jwt()["role"]
    
    if role != "admin":
        return jsonify({"message":"Unauthorized"}),401
    
    company = Company.query.get(cid)
    
    if company is None:
        return jsonify({"message": "Company Not Found"}), 404
    
    company.approval_status = "Approved"
    
    db.session.commit()
    
    return jsonify({"message": "Company Approved Successfully"}), 200


@admin.route("/admin/company/<int:cid>/reject", methods=["PUT"])
@jwt_required()
def reject_company(cid):
    
    uid = int(get_jwt_identity())
    role = get_jwt()["role"]
    
    if role != "admin":
        return jsonify({"message":"Unauthorized"}),401
    
    company = Company.query.get(cid)
    
    if company is None:
        return jsonify({"message":"Company Not Found"}),404
    
    company.approval_status = "Rejected"
    
    db.session.commit()
    
    return jsonify({"message":"Company Rejected Successfully"}),200

@admin.route("/admin/company/<int:cid>/blacklist", methods=["PUT"])
@jwt_required()
def blacklist_company(cid):
    
    uid = int(get_jwt_identity())
    role = get_jwt()["role"]
    
    if role != "admin":
        return jsonify({"message":"Unauthorized"}),401
    
    company = Company.query.get(cid)
    
    if company is None:
        return jsonify({"message": "Company Not Found"}), 404
    
    company.blacklisted = True
    
    db.session.commit()
    
    return jsonify({"message": "Company Blacklisted Successfully"}), 200


@admin.route("/admin/company/<int:cid>/unblacklist", methods=["PUT"])
@jwt_required()
def unblacklist_company(cid):
    
    uid = int(get_jwt_identity())
    role = get_jwt()["role"]
    
    if role != "admin":
        return jsonify({"message":"Unauthorized"}),401
    
    company = Company.query.get(cid)
    
    if company is None:
        return jsonify({"message": "Company Not Found"}), 404
    
    company.blacklisted = False
    
    db.session.commit()
    
    return jsonify({"message": "Company Unblacklisted Successfully"}), 200

@admin.route("/admin/drives", methods=["GET"])
@jwt_required()
def all_drives():
    
    uid = int(get_jwt_identity())
    role = get_jwt()["role"]
    
    if role != "admin":
        return jsonify({"message":"Unauthorized"}),401
        
    search = request.args.get("search", "")
    
    if search:
        drives = Drive.query.join(Company).filter(
            or_(
                Company.company_name.contains(search),
                Drive.job_title.contains(search),
                Drive.course.contains(search)
            )
        ).all()
    else:
        drives = Drive.query.all()
        
    
    data = []
    
    for drive in drives:
        data.append({
            "did": drive.did,
            "company": drive.company.company_name,
            "job_title": drive.job_title,
            "course": drive.course,
            "min_cgpa": drive.min_cgpa,
            "salary": drive.salary,
            "application_deadline": drive.application_deadline,
            "approval_status": drive.approval_status,
            "status": drive.status
        })
        
    return jsonify(data), 200

@admin.route("/admin/company/<int:cid>/drives", methods=["GET"])
@jwt_required()
def company_drives(cid):
    
    uid = int(get_jwt_identity())
    role = get_jwt()["role"]
    
    if role != "admin":
        return jsonify({"message":"Unauthorized"}),401
        
    company = Company.query.get(cid)
    
    if company is None:
        return jsonify({"message": "Company Not Found"}), 404
    
    search = request.args.get("search", "")
    
    if search:
        drives = Drive.query.filter(
            Drive.company_id == cid,
            or_(
                Drive.job_title.contains(search),
                Drive.description.contains(search),
                Drive.course.contains(search)
            )
        ).all()
    else:
        drives = Drive.query.filter_by(company_id=cid).all()
    
    data = []
    
    for drive in drives:
        data.append({
            "did": drive.did,
            "job_title": drive.job_title,
            "course": drive.course,
            "min_cgpa": drive.min_cgpa,
            "salary": drive.salary,
            "application_deadline": drive.application_deadline,
            "approval_status": drive.approval_status,
            "status": drive.status
        })
        
    return jsonify({
        "company": company.company_name,
        "drives": data
    }), 200

@admin.route("/admin/drive/<int:did>/applications", methods=["GET"])
@jwt_required()
def drive_applications(did):
    
    uid = int(get_jwt_identity())
    role = get_jwt()["role"]
    
    if role != "admin":
        return jsonify({"message":"Unauthorized"}),401
        
    drive = Drive.query.get(did)
    
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
            "student": application.student.name,
            "email": application.student.user.email,
            "phone": application.student.phone,
            "course": application.student.course,
            "cgpa": application.student.cgpa,
            "application_date": application.application_date,
            "status": application.status
        })
        
    return jsonify({
        "drive": drive.job_title,
        "company": drive.company.company_name,
        "applications": data
    }), 200

@admin.route("/admin/application/<int:aid>/history", methods=["GET"])
@jwt_required()
def application_history(aid):
    
    uid = int(get_jwt_identity())
    role = get_jwt()["role"]
    
    if role != "admin":
        return jsonify({"message":"Unauthorized"}),401
    
    application = Application.query.get(aid)
    
    if application is None:
        return jsonify({"message":"Application Not Found"}),404
    
    history = ApplicationHistory.query.filter_by(application_id=aid).order_by(ApplicationHistory.updated_at).all()
    
    data = []
    
    for h in history:
        data.append({
            "status": h.status,
            "feedback": h.feedback,
            "updated_at": h.updated_at
        })
        
    return jsonify(data),200