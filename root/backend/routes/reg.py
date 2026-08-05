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


@reg.route("/company/register", methods=["POST"])
def company_register():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")
    company_name = data.get("company_name")
    industry = data.get("industry")
    location = data.get("location")
    hr_contact = data.get("hr_contact")
    website = data.get("website")

    if not email or not password or not company_name:

        return jsonify({"message": "Required fields are missing."}), 400

    if User.query.filter_by(email=email).first():

        return jsonify({"message": "Email already exists."}), 400

    user = User(
        email=email,
        password=password,
        role="company"
    )

    db.session.add(user)
    db.session.commit()

    company = Company(
        user_id=user.uid,
        company_name=company_name,
        industry=industry,
        location=location,
        hr_contact=hr_contact,
        website=website
    )

    db.session.add(company)
    db.session.commit()

    return jsonify({"message": "Registration Successful. Waiting for Admin Approval."}), 201