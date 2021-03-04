from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import date, datetime


admin = 0

app = Flask(__name__)
app.secret_key = "swag"
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
            flash("Wrong password for admin!", 'error')
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
        if request.form['first_a'] and request.form['second_a']:
            start_date = datetime.strptime(request.form['first_a'], '%Y-%m-%d').date()
            second_date = datetime.strptime(request.form['second_a'], '%Y-%m-%d').date()
        else:
            flash("Your task doesn't have some of his alerts!", 'error')
            return redirect(url_for('manage'))

        if not name:
            flash("Your task doesn't have name!", 'error')
            return redirect(url_for('manage'))
        elif not shift:
            flash("Your task doesn't have shift!", 'error')
            return redirect(url_for('manage'))
        elif second_date < start_date:
            flash('Your period is negative!', 'error')
            return redirect(url_for('manage'))
        elif start_date < date.today():
            flash('Your first alert has passed!', 'error')
            return redirect(url_for('manage'))
        
        period = second_date - start_date
        period = period.days
        
        if name:
            new_task = Task(name, period, des, shift, start_date)
            db.session.add(new_task)
            db.session.commit()

        return render_template("manage.html", tasks=Task.query.all())

    else:
        return render_template("manage.html", tasks=Task.query.all())


@app.route('/edit/<my_task_id>', methods=['POST', 'GET'])
def edit(my_task_id):
    if request.method == 'POST':
        task = Task.query.filter_by(id=my_task_id)

        task_name_new = request.form.get('task_name_edit')
        task_bio_new = request.form.get('task_bio_edit')
        print(task_name_new)
        print(task_bio_new)
        print(1)

        '''if 'task_name_edit' in request.form:
            print('In')
        else:
            print('Out')
        '''
        '''if request.form['first_a'] and request.form['second_a']:
            start_date = datetime.strptime(request.form['first_a'], '%Y-%m-%d').date()
            second_date = datetime.strptime(request.form['second_a'], '%Y-%m-%d').date()
            if second_date < start_date:
                flash('Your period is negative!', 'error')
                return redirect(url_for('manage'))

            elif start_date < date.today():
                flash('Your first alert has passed!', 'error')
                return redirect(url_for('manage'))
            period = second_date - start_date
            task.period = period

        elif request.form['first_a']:
            flash("Your task doesn't have second alert", 'error')
            return redirect(url_for('manage'))

        elif request.form['second_a']:
            flash("Your task doesn't have first alert", 'error')
            return redirect(url_for('manage'))
'''
        if not task_name_new:
            flash("Your task doesn't have name!", 'error')
            return redirect(url_for('manage'))
        elif not task_bio_new:
            flash("Your task doesn't have shift!", 'error')
            return redirect(url_for('manage'))

        if request.form.get('shift'):
            task_shift_new = request.form.get('shift')
            task.shift = task_shift_new

        task.name = task_name_new
        task.description = task_bio_new

        print(task.name)
        print(task.description)

        db.session.commit()
        return redirect(url_for('manage'))
    else:
        return redirect(url_for('manage'))


@app.route('/delete/<task_id>', methods=['POST', 'GET'])
def delete(task_id):
    if request.method == 'POST':
        print(task_id)
        Task.query.filter_by(id=task_id).delete()
        db.session.commit()

        return redirect(url_for('manage'))
    else:
        return redirect(url_for('manage'))



if __name__ == '__main__':
    app.run(debug=True)