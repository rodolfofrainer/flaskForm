from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, flash
from flask_mail import Mail, Message
from datetime import datetime

app = Flask(__name__)

app.config["SECRET_KEY"] = "myapplication123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'rodolfofrainerautomated'
app.config["MAIL_PASSWORD"] = 'bzccglrarhqghkuo'

db = SQLAlchemy(app)

mail = Mail(app)


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(255))
    date_created = db.Column(db.Date)
    occupation = db.Column(db.String(25))


@ app.route('/', methods=["GET", "POST"])
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

        message_body = f'Thanks for you submission, {first_name}'
        f"""Here is your data:
            First Name: {first_name.title()}
            Last Name: {last_name.title()}
            Email:{email}
            Date: {date_obj}
            Occupation: {occupation}"""
        message = Message(subject='New form submission',
                          sender=app.config["MAIL_USERNAME"],
                          recipients=[email],
                          body=message_body)
        try:
            mail.send(message)
            flash(
                f'{first_name.title()}, Your form was submitted successfully', 'success')
        except Exception as e:
            print(f"An error occurred while sending the email: {e}")
            flash(
                "There was an error submitting your form. Please try again later.", "danger")

    return render_template('index.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)
