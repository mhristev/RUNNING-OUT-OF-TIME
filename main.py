from time import sleep, time

from flask import render_template, request, url_for, redirect, flash
from datetime import date, datetime, timedelta
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user
from dateutil.relativedelta import relativedelta

from models import User, Task, db, Done_Task, app, Temporary_Task

from flask_mail import Mail, Message

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ruski11v@gmail.com'
app.config['MAIL_PASSWORD'] = 'Ruski5500'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route('/', methods=['POST', 'GET'])
def home():
   # msg = Message('Hello', sender="ruski11v@gmail.com", recipients=['mhristev03@gmail.com'])
   # msg.body = 'Testing email sending'
    #mail.send(msg)



    nowbro = datetime.now().replace(microsecond=0, hour=0, second=0, minute=0)
    b = timedelta(days=1)
    yesterday = nowbro - b 
    tasks_up=Task.query.filter_by(next_alert=yesterday)

    for t in tasks_up:
        t.next_alert += timedelta(days=t.period);
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
        return render_template('index.html', tasks=Task.query.filter_by(next_alert=today_d), temp_tasks=Temporary_Task.query.filter_by(date=today_d))


@app.route('/admin')
@login_required
def admin():
    today_d = datetime.now().replace(microsecond=0, hour=0, second=0, minute=0)
    return render_template("admin.html", tasks=Task.query.filter_by(next_alert=today_d), temp_tasks=Temporary_Task.query.filter_by(date=today_d))


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
        if request.form.get('temporary_task_name') and request.form.get('temporary_task_des'):
            temp_task_name = request.form.get('temporary_task_name')
            temp_task_des = request.form.get('temporary_task_des')

            new_task = Temporary_Task(temp_task_name, temp_task_des, date.today())
            db.session.add(new_task)
            db.session.commit()

        else:
            flash('Temporary task invalid!', 'error')
            return redirect(url_for('home'))

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
        done_task = Done_Task(person_name, task.name)

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


if __name__ == '__main__':
    app.run(debug=True)
