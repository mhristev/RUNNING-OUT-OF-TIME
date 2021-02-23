from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import date
admin = 0

app = Flask(__name__)
file_path = os.path.abspath(os.getcwd())+"/my404_database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(75), nullable=False, unique=True)
    period = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(150), nullable=False, unique=True)
    shift = db.Column(db.String(6), nullable=False)

    done_by = db.Column(db.String(150))
    #done_date = db.Column(db.DateTime)


    def __init__(self, name, period, description, shift):
        self.name = name
        self.period = period
        self.description = description
        self.shift = shift

    def is_active(self):
        return True

'''class done_Task:
    done_date
    person_name
    task_name
'''

db.create_all()
@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        password = request.form.get('admin')
        if password == 'admin':
            global admin
            admin = 1
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('home'))


    else:
        return render_template("index.html")



@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if admin == 1:
        return render_template("admin.html")
    else:
        return redirect(url_for('home'))


@app.route('/select', methods=['POST', 'GET'])
def select():
    return render_template("select.html")

@app.route('/manage', methods=['POST', 'GET'])
def manage():
    if request.method == 'POST':
        name = request.form.get('name')
        des = request.form.get('description')
        shift = request.form.get('shift')
        first_a = request.form.get('first_a')
        second_a = request.form.get('second_a')

        First_A = [int(x) for x in first_a.split('/') if x.strip()]
        Second_A = [int(x) for x in second_a.split('/') if x.strip()]
        d0 = date(First_A[2], First_A[1], First_A[0])
        d1 = date(Second_A[2], Second_A[1], Second_A[0])
        period = abs((d1 - d0).days)
        print(period)

        if name and des and shift:
            new_task = Task(name, period, des, shift)
            db.session.add(new_task)
            db.session.commit()

        return render_template("manage.html")

    else:
        return render_template("manage.html")


if __name__ == '__main__':
    app.run()