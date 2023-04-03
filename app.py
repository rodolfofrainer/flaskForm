import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db = SQLAlchemy(app)


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(255))
    date_created = db.Column(db.Date)
    occupation = db.Column(db.String(25))


@app.route('/', methods=["GET", "POST"])
def index():
    print(request.method)
    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        date = request.form['date']
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        occupation = request.form['occupation']

        form = Form(
            first_name=first_name,
            last_name=last_name,
            email=email,
            date_created=date_obj,
            occupation=occupation
        )
        db.session.add(form)
        db.session.commit()
    return render_template('index.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)
