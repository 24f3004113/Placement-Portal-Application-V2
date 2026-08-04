from flask import Flask
from db import db, User, Company, Student, Drive, Application, Placement

app = Flask(__name__)

if __name__ == "__main__":

    app.run(debug=True)