from time import sleep

from flask import render_template, request, url_for, redirect, flash
from datetime import date, datetime
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user

from models import User, Task, db, Done_Task, app

from flask_mail import Mail, Message

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'email'
app.config['MAIL_PASSWORD'] = 'pass'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route('/', methods=['POST', 'GET'])
def home():

    #msg = Message('Hello', sender=app.config.get("MAIL_USERNAME"), recipients=[''])
    #msg.body = 'Testing email sending'
    #mail.send(msg)
    #sleep(5)
    #mail.send(msg)

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
        return render_template('index.html', tasks=Task.query.filter_by(next_alert=today_d))




@app.route('/admin')
@login_required
def admin():
    today_d = datetime.now().replace(microsecond=0, hour=0, second=0, minute=0)
    return render_template("admin.html", tasks=Task.query.filter_by(next_alert=today_d))



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


        if request.form['first_a'] and request.form['second_a']:
            start_date = datetime.strptime(request.form['first_a'], '%Y-%m-%d').date()
            second_date = datetime.strptime(request.form['second_a'], '%Y-%m-%d').date()
        else:
            flash("Your task doesn't have some of its alerts!", 'error')
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
@login_required
def edit(my_task_id):
    if request.method == 'POST':
        task = Task.query.filter_by(id=my_task_id).first()

        task_name_new = request.form.get('task_name_edit')
        task_bio_new = request.form.get('task_bio_edit')

        if 'first_alert_edit' in request.form and 'second_alert_edit' in request.form:
            start_date = datetime.strptime(request.form['first_alert_edit'], '%Y-%m-%d').date()
            second_date = datetime.strptime(request.form['second_alert_edit'], '%Y-%m-%d').date()

            if second_date < start_date:
                flash('Your period is negative!', 'error')
                return redirect(url_for('manage'))

            elif start_date < date.today():
                flash('Your first alert has passed!', 'error')
                return redirect(url_for('manage'))

            period = second_date - start_date
            period = period.days
            task.period = period
            task.next_alert = start_date


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

        db.session.commit()
        return redirect(url_for('manage'))
    else:
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