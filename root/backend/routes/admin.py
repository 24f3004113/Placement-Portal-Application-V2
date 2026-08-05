from flask import Blueprint, jsonify, session
from db import User, Company, Student, Drive, Application

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

