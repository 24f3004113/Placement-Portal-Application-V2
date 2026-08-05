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

