from flask import Flask
from db import db, User, Company, Student, Drive, Application, Placement

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///placement.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "lokaproject"

db.init_app(app)

with app.app_context():
    db.create_all()
    
    admin = User.query.filter_by(role="admin").first()
    
    if admin is None:
        admin = User(email="admin@placement.com",password="admin123",role="admin")
        
        db.session.add(admin)
        db.session.commit()


app.route("/")
def home():
    return "Placement Portal"


if __name__ == "__main__":
    app.run(debug=True)