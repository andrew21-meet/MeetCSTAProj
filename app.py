from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'very secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/andre/Desktop/start/database.db'
Bootstrap(app)
db = SQLAlchemy(app)
# login_manager = LoginManager()     DOESNT WORK ANYMORE
# login_manager.init_app(app)     DOESNT WORK ANYMORE
# login_manager.login_View = 'login'     DOESNT WORK ANYMORE


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(80))


# @login_manager.user_loader     DOESNT WORK ANYMORE
# def load_user(user_id):     DOESNT WORK ANYMORE
#     return User.query.get(int(user_id))     DOESNT WORK ANYMORE
#      DOESNT WORK ANYMORE

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'Post'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.password == form.password.data:
                # login_user(user, remember=form.remember.data)     DOESNT WORK ANYMORE
                return redirect(url_for('weather'))

        return '<h1>Invalid Username or Password</h1>'
        # this is for testing if the form works
        # return '<h1>' + form.username.data + '-' + form.password.data + '<h1>'

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'Post'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>new account has been created</h1>'
        # this is for testing if the form works
        # return '<h1>' + form.username.data + '-' + form.email.data + '-' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)


@app.route('/weather', methods=['GET', 'POST'])
# @login_required      DOESNT WORK ANYMORE
def weather():

    # if the "get weather" button isnt pressed, go to weather.html. if it is, go to results.html
    if request.method == "POST":
        city = request.form['city']
        country = request.form['country']
        api_key = "1311fcb4b7fac0d074b20a09862788b6"

        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?appid={api_key}&q={city},{country}&units=metric')

        if response.status_code == 404:
            return render_template('weather.html')

        weather_data = response.json()

        temp = round(weather_data['main']['temp'])
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        # pass all variables to results.html
        return render_template("results.html", temp=temp, humidity=humidity, wind_speed=wind_speed, city=city)

    return render_template('weather.html')


if __name__ == '__main__':
    app.run(debug=True)
