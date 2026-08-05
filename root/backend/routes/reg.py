from flask import Blueprint, request, jsonify
from db import db, User, Student, Company

reg = Blueprint("reg", __name__)

@reg.route("/student/register", methods=["POST"])
def student_register():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")
    name = data.get("name")
    phone = data.get("phone")
    course = data.get("course")
    cgpa = data.get("cgpa")
    graduation_year = data.get("graduation_year")
    skills = data.get("skills")
    resume = data.get("resume")

    if not email or not password or not name:

        return jsonify({"message": "Required fields are missing."}), 400

    if User.query.filter_by(email=email).first():

        return jsonify({"message": "Email already exists."}), 400

    user = User(
        email=email,
        password=password,
        role="student"
    )

    db.session.add(user)
    db.session.commit()

    student = Student(
        user_id=user.uid,
        name=name,
        phone=phone,
        course=course,
        cgpa=cgpa,
        graduation_year=graduation_year,
        skills=skills,
        resume=resume
    )

    db.session.add(student)
    db.session.commit()

    return jsonify({"message": "Student Registered Successfully."}), 201