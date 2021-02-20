from flask import Flask, render_template, request, url_for, redirect



app = Flask(__name__)



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
    return render_template("manage.html")


if __name__ == '__main__':
    app.run()