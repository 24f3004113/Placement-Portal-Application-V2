from flask import Blueprint, request, jsonify, session
from db import User, Company, Student

login = Blueprint("login", __name__)

@login.route("/login", methods=["POST"])
def user_login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:

        return jsonify({"message": "Email and Password are required."}), 400

    user = User.query.filter_by(email=email,password=password).first()

    if user is None:

        return jsonify({"message": "Invalid Email or Password."}), 401

    if user.role == "admin":

        session["uid"] = user.uid
        session["role"] = "admin"

        return jsonify({"message": "Admin Login Successful"}), 200

    elif user.role == "company":

        company = Company.query.filter_by(user_id=user.uid).first()

        if not company.approved:

            return jsonify({"message": "Company approval pending."}), 403

        if company.blacklisted:

            return jsonify({"message": "Company account is blacklisted."}), 403

        session["uid"] = user.uid
        session["role"] = "company"

        return jsonify({"message": "Company Login Successful"}), 200

    elif user.role == "student":

        student = Student.query.filter_by(user_id=user.uid).first()

        if student.blacklisted:

            return jsonify({"message": "Student account is blacklisted."}), 403

        session["uid"] = user.uid
        session["role"] = "student"

        return jsonify({"message": "Student Login Successful"}), 200