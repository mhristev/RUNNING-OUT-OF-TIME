from time import sleep, time

from flask import render_template, request, url_for, redirect, flash
from datetime import date, datetime, timedelta
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from dateutil.relativedelta import relativedelta

from models import User, Task, db, DoneTask, app, TemporaryTask, MissedTask

from flask_mail import Mail, Message

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ruski11v@gmail.com'
app.config['MAIL_PASSWORD'] = 'Ruski5500'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

today = None

@app.route('/', methods=['POST', 'GET'])
def home():
    # msg = Message('Hello', sender="ruski11v@gmail.com", recipients=['mhristev03@gmail.com'])
    # msg.body = 'Testing email sending'
    # mail.send(msg)

    nowbro = datetime.now().replace(microsecond=0, hour=0, second=0, minute=0)
    b = timedelta(days=1)
    yesterday = nowbro - b 
    tasks_up = Task.query.filter_by(next_alert=yesterday)

    first = True
    for task in tasks_up:
        if task.column_id == 3:
            done_task = DoneTask(task.person_name, task.name)
            db.session.add(done_task)
        elif task.column_id == 2 or task.column_id == 1:
            missed_task = MissedTask(task.name)
            db.session.add(missed_task)

        db.session.commit()

    global today
    if today != datetime.now().replace(microsecond=0, hour=0, second=0, minute=0) and datetime.today().day == 1:
        today = datetime.now().replace(microsecond=0, hour=0, second=0, minute=0)
        msg = Message('Ненаправени дейности', sender="ruski11v@gmail.com", recipients=['mhristev03@gmail.com'])
        msg_body = ''

        missed_tasks = MissedTask.query.all()
        for task in missed_tasks:
            msg_body += 'Име: ' + task.name + "; Ден: " + task.missed_date + '\n'

        msg.body = msg_body
        mail.send(msg)

    for task in tasks_up:
        task.next_alert += timedelta(days=t.period);
        db.session.commit()

    if request.method == 'POST':
        password = request.form.get('password')

        test = User.query.filter_by(id=1).first()

        if test and check_password_hash(test.password, password):
            login_user(test)
            return redirect(url_for('admin'))
        else:
            flash("Wrong password for admin!", 'error')
            return redirect(url_for('home'))
    else:
        today_d = datetime.now().replace(microsecond=0, hour=0, second=0, minute=0)
        #tasks_id1 = Task.query.filter_by(next_alert=today_d)
        tasks_id1 = Task.query.filter_by(next_alert=today_d, column_id=1)
        tasks_id2 = Task.query.filter_by(next_alert=today_d, column_id=2)
        tasks_id3 = Task.query.filter_by(next_alert=today_d, column_id=3)

        temp_tasks_id1 = TemporaryTask.query.filter_by(date=today_d, column_id=1)
        temp_tasks_id2 = TemporaryTask.query.filter_by(date=today_d, column_id=2)
        temp_tasks_id3 = TemporaryTask.query.filter_by(date=today_d, column_id=3)

        return render_template('index.html', tasks1=tasks_id1, tasks2=tasks_id2, tasks3=tasks_id3, temp_tasks1=temp_tasks_id1, temp_tasks2=temp_tasks_id2, temp_tasks3=temp_tasks_id3)


@app.route('/admin')
@login_required
def admin():
    today_d = datetime.now().replace(microsecond=0, hour=0, second=0, minute=0)

    tasks_id1 = Task.query.filter_by(next_alert=today_d, column_id=1)
    tasks_id2 = Task.query.filter_by(next_alert=today_d, column_id=2)
    tasks_id3 = Task.query.filter_by(next_alert=today_d, column_id=3)

    temp_tasks_id1 = TemporaryTask.query.filter_by(date=today_d, column_id=1)
    temp_tasks_id2 = TemporaryTask.query.filter_by(date=today_d, column_id=2)
    temp_tasks_id3 = TemporaryTask.query.filter_by(date=today_d, column_id=3)

    return render_template('admin.html', tasks1=tasks_id1, tasks2=tasks_id2, tasks3=tasks_id3,
                           temp_tasks1=temp_tasks_id1, temp_tasks2=temp_tasks_id2, temp_tasks3=temp_tasks_id3)


@app.route('/select', methods=['POST', 'GET'])
@login_required
def select():
    return render_template("select.html")


@app.route('/manage', methods=['POST', 'GET'])
@login_required
def manage():
    if request.method == 'POST':
        name = request.form.get('name')
        des = request.form.get('description')
        shift = request.form.get('shift')

        if request.form['first_a'] and request.form['period']:
            start_date = datetime.strptime(request.form['first_a'], '%Y-%m-%d').date()
            period = request.form['period']
            period_type = request.form['period_type']


            period = int(period)

            if period_type == 'Месеца':
                next_alert = start_date + relativedelta(months=+period)
                period = next_alert - start_date
                period = period.days
                # second_date = datetime.strptime(request.form['second_a'], '%Y-%m-%d').date()
            else:
                next_alert = start_date + timedelta(days=period)
                

        if name:
            new_task = Task(name, period, des, shift, start_date)
            db.session.add(new_task)
            db.session.commit()

        return render_template("manage.html", tasks=Task.query.all())

    else:
        return render_template("manage.html", tasks=Task.query.all())


@app.route('/add_temp', methods=['POST', 'GET'])
def add_temp_task():
    if request.method == 'POST':
        if request.form.get('temporary_task_name'):
            temp_task_name = request.form.get('temporary_task_name')

            new_task = TemporaryTask(temp_task_name)
            if request.form.get('temporary_task_des'):
                temp_task_des = request.form.get('temporary_task_des')
                new_task.description = temp_task_des

            db.session.add(new_task)
            db.session.commit()

    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('home'))


@app.route('/edit/<my_task_id>', methods=['POST', 'GET'])
@login_required
def edit(my_task_id):
    if request.method == 'POST':
        task = Task.query.filter_by(id=my_task_id).first()

        task_name_new = request.form.get('task_name_edit')
        task_bio_new = request.form.get('task_bio_edit')

        if request.form.get('first_alert_edit') == None:
            task.name = task_name_new
            task.description = task_bio_new
            db.session.commit()
            return redirect(url_for('manage'))

        
        start_date = datetime.strptime(request.form['first_alert_edit'], '%Y-%m-%d').date()
        period = request.form['period']
        period_type = request.form['period_type']


        period = int(period)

        if period_type == 'Месеца':
                next_alert = start_date + relativedelta(months=+period)
                period = next_alert - start_date
                period = period.days
                print(period)
                print(next_alert)
        else:
            next_alert = start_date + timedelta(days=period)
            print(next_alert)


        task.period = period
        task.next_alert = start_date

        if request.form.get('shift'):
            task_shift_new = request.form.get('shift')
            task.shift = task_shift_new

        task.name = task_name_new
        task.description = task_bio_new

        db.session.commit()

        return redirect(url_for('manage'))
    else:
        print("bro");
        return redirect(url_for('manage'))


@app.route('/delete/<task_id>', methods=['POST', 'GET'])
@login_required
def delete(task_id):
    if request.method == 'POST':
        Task.query.filter_by(id=task_id).delete()
        db.session.commit()

        return redirect(url_for('manage'))
    else:
        return redirect(url_for('manage'))


@app.route('/send/<task_id>', methods=['POST', 'GET'])
def send(task_id):
    if request.method == 'POST':
        task = Task.query.filter_by(id=task_id).first()
        person_name = request.form.get('person_name')
        done_task = DoneTask(person_name, task.name)

        db.session.add(done_task)
        db.session.commit()

        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/movedtask3', methods=['POST'])
def task_column3():

    task_id = request.form['javascript_data']
    person_name = request.form['personName']

    print('In moved 3' + person_name)

    task = Task.query.filter_by(id=task_id).first()
    task.column_id = 3
    task.person_name = person_name

    db.session.commit()

    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('home'))


@app.route('/movedtask2', methods=['POST'])
def task_column2():
    task_id = request.form['javascript_data']
    person_name = request.form['personName']

    task = Task.query.filter_by(id=task_id).first()
    task.column_id = 2
    task.person_name = person_name

    db.session.commit()

    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('home'))


@app.route('/movedtask1', methods=['POST'])
def task_column1():
    task_id = request.form['javascript_data']
    task = Task.query.filter_by(id=task_id).first()
    task.column_id = 1
    db.session.commit()

    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('home'))


@app.route('/movedtemptask3', methods=['POST'])
def tasktemp_column3():
    task_id = request.form['javascript_data']

    person_name = request.form['personName']

    print('In moved temp 3')
    print(person_name)

    task = TemporaryTask.query.filter_by(id=task_id).first()
    task.column_id = 3
    db.session.commit()

    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('home'))


@app.route('/movedtemptask2', methods=['POST'])
def tasktemp_column2():
    task_id = request.form['javascript_data']
    person_name = request.form['personName']
    task = TemporaryTask.query.filter_by(id=task_id).first()
    task.column_id = 2
    task.person_name = person_name

    db.session.commit()

    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('home'))


@app.route('/movedtemptask1', methods=['POST'])
def tasktemp_column1():
    task_id = request.form['javascript_data']
    task = TemporaryTask.query.filter_by(id=task_id).first()
    task.column_id = 1
    db.session.commit()

    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True)
