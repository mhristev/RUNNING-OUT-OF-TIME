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
    #name = db.Column(db.String(150), nullable=False, unique=True)
    how_often = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(150), nullable=False, unique=True)
    done_by = db.Column(db.String(150))

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

        '''newtask_description = request.form.get('description')
        newtask_how_often = request.form.get('how_often')
        if newtask_description and newtask_how_often:
            new_task = Task(newtask_how_often, description)
            db.session.add(new_task)
            db.session.commit()
        '''


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
    return render_template("manage.html")


if __name__ == '__main__':
    app.run()