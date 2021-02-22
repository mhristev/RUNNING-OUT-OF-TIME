from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
file_path = os.path.abspath(os.getcwd())+"/my404_database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    how_often = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(150), nullable=False, unique=True)
    done_by = db.Column(db.String(150))
    #done_date = db.Column(db.DateTime)


    def __init__(self, how_often, description):
        self.how_often = how_often
        self.description = description

    def is_active(self):
        return True

db.create_all()
@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        password = request.form.get('admin')
        if password == 'admin':
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('home'))


    else:
        return render_template("index.html")



@app.route('/admin', methods=['POST', 'GET'])
def admin():
    return render_template("admin.html")


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
        print(first_a)
        print(second_a)
        #period = second_a - first_a
        #print(period)
        if name and des and shift:
            new_task = Task(des, shift)
            db.session.add(new_task)
            db.session.commit()

        return render_template("manage.html")

    else:
        return render_template("manage.html")


if __name__ == '__main__':
    app.run()