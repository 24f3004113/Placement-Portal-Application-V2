from flask import Blueprint, jsonify, session
from db import db, User, Company, Student, Drive, Application

admin = Blueprint("admin", __name__)

@admin.route("/admin/dashboard", methods=["GET"])
def admin_dashboard():
    
    if "uid" not in session or session["role"] != "admin":
        return jsonify({"message": "Unauthorized"}), 401
    
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
def all_students():
    
    if "uid" not in session or session["role"] != "admin":
        return jsonify({"message": "Unauthorized"}), 401
    
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
def all_companies():
    if "uid" not in session or session["role"] != "admin":
        return jsonify({"message": "Unauthorized"}), 401
        
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
            "approved": company.approved,
            "blacklisted": company.blacklisted
        })
        
    return jsonify(data), 200

@admin.route("/admin/company/pending", methods=["GET"])
def pending_companies():
    
    if "uid" not in session or session["role"] != "admin":
        return jsonify({"message": "Unauthorized"}), 401
        
    companies = Company.query.filter_by(approved=False).all()
    
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
def approve_company(cid):
    
    if "uid" not in session or session["role"] != "admin":
        return jsonify({"message": "Unauthorized"}), 401
    
    company = Company.query.get(cid)
    
    if company is None:
        return jsonify({"message": "Company Not Found"}), 404
    
    company.approved = True
    
    db.session.commit()
    
    return jsonify({"message": "Company Approved Successfully"}), 200

@admin.route("/admin/company/<int:cid>/blacklist", methods=["PUT"])
def blacklist_company(cid):
    
    if "uid" not in session or session["role"] != "admin":
        return jsonify({"message": "Unauthorized"}), 401
    
    company = Company.query.get(cid)
    
    if company is None:
        return jsonify({"message": "Company Not Found"}), 404
    
    company.blacklisted = True
    
    db.session.commit()
    
    return jsonify({"message": "Company Blacklisted Successfully"}), 200
