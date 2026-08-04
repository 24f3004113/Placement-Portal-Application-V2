from flask import Flask
from db import db, User, Company, Student, Drive, Application, Placement

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///placement.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "lokaproject"


if __name__ == "__main__":

    app.run(debug=True)