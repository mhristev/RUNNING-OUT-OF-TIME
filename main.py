from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import date, datetime
admin = 0

app = Flask(__name__)
file_path = os.path.abspath(os.getcwd())+"/database.db"
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
        today_d = datetime.now().replace(microsecond=0, hour=0, second=0, minute=0)
        return render_template('index.html', tasks=Task.query.filter_by(next_alert=today_d))



@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if admin == 1:
        today_d = datetime.now().replace(microsecond=0, hour=0, second=0, minute=0)
        return render_template("admin.html", tasks=Task.query.filter_by(next_alert=today_d))
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
        start_date = datetime.strptime(request.form['first_a'], '%Y-%m-%d').date()
        second_date = datetime.strptime(request.form['second_a'], '%Y-%m-%d').date()
        
        
        period = second_date - start_date
        period = period.days
        
        if name:
            new_task = Task(name, period, des, shift, start_date)
            db.session.add(new_task)
            db.session.commit()

        return render_template("manage.html", tasks=Task.query.all())

    else:
        return render_template("manage.html", tasks=Task.query.all())


if __name__ == '__main__':
    app.run()