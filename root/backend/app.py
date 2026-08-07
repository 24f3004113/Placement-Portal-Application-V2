from flask import Flask, Blueprint
from db import db, User, Company, Student, Drive, Application
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///placement.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "lokaproject"
app.config["JWT_SECRET_KEY"] = "loka_jwt_secret_key_extended_for_no_warning"

jwt = JWTManager(app)

db.init_app(app)

with app.app_context():
    db.create_all()
    
    admin = User.query.filter_by(role="admin").first()
    
    if admin is None:
        admin = User(email="admin@placement.com",password="admin123",role="admin")
        
        db.session.add(admin)
        db.session.commit()

from routes.reg import reg
app.register_blueprint(reg)

from routes.login import login
app.register_blueprint(login)

from routes.admin import admin
app.register_blueprint(admin)

from routes.company import company
app.register_blueprint(company)

from routes.student import student
app.register_blueprint(student)



@app.route("/")
def home():
    return "Placement Portal"


if __name__ == "__main__":
    app.run(debug=True)