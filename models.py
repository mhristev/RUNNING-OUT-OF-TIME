from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from flask_security import UserMixin
import os
import email_validator
from datetime import date, datetime

app = Flask(__name__)

app.secret_key = "swag"
login_manager = LoginManager(app)

file_path = os.path.abspath(os.getcwd()) + "/database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@login_manager.user_loader
def get_user(id):
    return User.query.filter_by(id=id).first()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, password):
        self.password = generate_password_hash(password)

    def is_active(self):
        return True


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(75), nullable=False)
    period = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(150))
    shift = db.Column(db.String(6), nullable=False)
    next_alert = db.Column(db.DateTime)
    column_id = db.Column(db.Integer, nullable=False)

    def __init__(self, name, period, description, shift, next_alert):
        self.name = name
        self.period = period
        self.description = description
        self.shift = shift
        self.next_alert = next_alert
        self.column_id = 1

class TemporaryTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(75), nullable=False)
    description = db.Column(db.String(150))
    date = db.Column(db.DateTime)
    column_id = db.Column(db.Integer, nullable=False)

    def __init__(self, name, description, date):
        self.name = name
        self.description = description
        self.date = date
        self.column_id = 1

class DoneTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    done_date = db.Column(db.DateTime(timezone=True))
    person_name = db.Column(db.String(150), nullable=False)
    task_name = db.Column(db.String(75), nullable=False)

    def __init__(self, person_date, task_name):
        self.done_date = datetime.datetime.today().replace(microsecond=0)
        self.person_name = person_date
        self.task_name = task_name


db.create_all()

main_admin = User('admin')
db.session.add(main_admin)
db.session.commit()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('home'))
