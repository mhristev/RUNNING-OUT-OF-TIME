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

file_path = os.path.abspath(os.getcwd()) + "/WebApp/database.db"
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
    person_name = db.Column(db.String(75), nullable=True)

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
    person_name = db.Column(db.String(75), nullable=True)

    def __init__(self, name):
        self.name = name
        self.date = datetime.now().replace(microsecond=0, hour=0, second=0, minute=0)
        self.column_id = 1


class DoneTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_for_temp = db.Column(db.Integer, nullable=True)
    done_date = db.Column(db.DateTime(timezone=True))
    person_name = db.Column(db.String(150), nullable=False)
    task_name = db.Column(db.String(75), nullable=True)

    def __init__(self, person_name, task_name, task_date):
        self.done_date = task_date
        self.person_name = person_name
        self.task_name = task_name


class MissedTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_for_temp = db.Column(db.Integer, nullable=True)
    missed_date = db.Column(db.DateTime(timezone=True))
    task_name = db.Column(db.String(75), nullable=True)

    def __init__(self, task_name, task_date):
        self.missed_date = task_date
        self.task_name = task_name



class MailDate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    next_date = db.Column(db.DateTime(timezone=True))

    def __init__(self, date):
        self.next_date = date

db.create_all()

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('home'))
