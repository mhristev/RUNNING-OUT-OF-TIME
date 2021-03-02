from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import date, datetime
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
    next_alert = db.Column(db.DateTime)

    done_by = db.Column(db.String(150), nullable=True)
    #done_date = db.Column(db.DateTime)


    def __init__(self, name, period, description, shift, next_alert):
        self.name = name
        self.period = period
        self.description = description
        self.shift = shift
        self.next_alert = next_alert

    def is_active(self):
        return True

class done_Task:
    done_date = db.Column(db.DateTime(timezone=True))
    person_name = db.Column(db.String(150), nullable=False)
    task_name = db.Column(db.String(75), nullable=False, unique=True)

    def __init__(self, person_date, task_name):
        self.done_date = datetime.datetime.today().replace(microsecond=0)
        self.person_name = person_date
        self.task_name = task_name


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
        today = date.today()
        '''tasks = Task.query.all()
        tasks_html = []
        for task in tasks:
            if task.next_alert == today:
                task.next_alert += datetime.timedelta(days=task.period)
                tasks_html.append(task)'''


        return render_template('index.html', tasks=Task.query.all())



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
        #first_a = request.form.get('first_a')
        #second_a = request.form.get('second_a')

        #First_A = [int(x) for x in first_a.split('/') if x.strip()]
        #Second_A = [int(x) for x in second_a.split('/') if x.strip()]
        #d0 = date(First_A[2], First_A[1], First_A[0])
        #d1 = date(Second_A[2], Second_A[1], Second_A[0])
        #period = abs((d1 - d0).days)

        #startdate = datetime.date(request.form['first_a'])

        #print(startdate)

        print(name)
        #print(period)
        print(des)
        print(shift)
        #print(first_a)
        if name and des and shift:
            #new_task = Task(name, period, des, shift, first_a)
            #db.session.add(new_task)
            db.session.commit()

        return render_template("manage.html")

    else:
        return render_template("manage.html")


if __name__ == '__main__':
    app.run()