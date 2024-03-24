from flask import Flask,render_template,url_for,request,jsonify,redirect
from flask_cors import cross_origin
import pandas as pd
import numpy as np
import datetime
import pickle
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

app = Flask(__name__, template_folder="template")
model = pickle.load(open("./models/cat.pkl", "rb"))
print("Model Loaded")
# app=Flask(__name__) # unique name
# file=open("model.pkl","rb")
# random_Forest=pickle.load(file)
# file.close()

# Tells flask-sqlalchemy what database to connect to
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
# Enter a secret key
app.config["SECRET_KEY"] = "secretkey12"
# Initialize flask-sqlalchemy extension
db = SQLAlchemy()


login_manager = LoginManager()
login_manager.init_app(app)


# Create user model
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True,
                         nullable=False)
    password = db.Column(db.String(250),
                         nullable=False)
    
# Initialize app with extension
db.init_app(app)
# Create database within app context
 
with app.app_context():
    db.create_all()


# Creates a user loader callback that returns the user object given an id
@login_manager.user_loader
def loader_user(user_id):
	return Users.query.get(user_id)





@app.route("/",methods=['GET'])
@cross_origin()
def home():
	return render_template("index.html")


@app.route("/register" , methods=["GET", "POST"])
def register():
	
    if request.method == "POST":
        user = Users(username=request.form.get("username"),
                    password=request.form.get("password"))
        # Add the user to the database
        db.session.add(user)
        # Commit the changes made
        db.session.commit()
        # Once user account created, redirect them
        # to login route (created later on)
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login" , methods=["GET", "POST"])
def login():
    # If a post request was made, find the user by
    # filtering for the username
    if request.method == "POST":
        user = Users.query.filter_by(
            username=request.form.get("username")).first()
        # Check if the password entered is the
        # same as the user's password
        if user.password == request.form.get("password"):
            # Use the login_user method to log in the user
            login_user(user)
            return render_template("predictor.html")
    return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    return render_template("index.html")

# @app.route("/predict", methods=["GET","POST"])
# @cross_origin()
# def predict():
#     if request.method=="POST":
#         return render_template('predictor.html')


@app.route("/result",methods=['GET', 'POST'])
@cross_origin()
def result():
	if request.method == "POST":
		# DATE
		date = request.form['date']
		day = float(pd.to_datetime(date, format="%Y-%m-%dT").day)
		month = float(pd.to_datetime(date, format="%Y-%m-%dT").month)
		# MinTemp
		minTemp = float(request.form['mintemp'])
		# MaxTemp
		maxTemp = float(request.form['maxtemp'])
		# Rainfall
		rainfall = float(request.form['rainfall'])
		# Evaporation
		evaporation = float(request.form['evaporation'])
		# Sunshine
		sunshine = float(request.form['sunshine'])
		# Wind Gust Speed
		windGustSpeed = float(request.form['windgustspeed'])
		# Wind Speed 9am
		windSpeed9am = float(request.form['windspeed9am'])
		# Wind Speed 3pm
		windSpeed3pm = float(request.form['windspeed3pm'])
		# Humidity 9am
		humidity9am = float(request.form['humidity9am'])
		# Humidity 3pm
		humidity3pm = float(request.form['humidity3pm'])
		# Pressure 9am
		pressure9am = float(request.form['pressure9am'])
		# Pressure 3pm
		pressure3pm = float(request.form['pressure3pm'])
		# Temperature 9am
		temp9am = float(request.form['temp9am'])
		# Temperature 3pm
		temp3pm = float(request.form['temp3pm'])
		# Cloud 9am
		cloud9am = float(request.form['cloud9am'])
		# Cloud 3pm
		cloud3pm = float(request.form['cloud3pm'])
		# Cloud 3pm
		location = float(request.form['location'])
		# Wind Dir 9am
		winddDir9am = float(request.form['winddir9am'])
		# Wind Dir 3pm
		winddDir3pm = float(request.form['winddir3pm'])
		# Wind Gust Dir
		windGustDir = float(request.form['windgustdir'])
		# Rain Today
		rainToday = float(request.form['raintoday'])

		input_lst = [location , minTemp , maxTemp , rainfall , evaporation , sunshine ,
					 windGustDir , windGustSpeed , winddDir9am , winddDir3pm , windSpeed9am , windSpeed3pm ,
					 humidity9am , humidity3pm , pressure9am , pressure3pm , cloud9am , cloud3pm , temp9am , temp3pm ,
					 rainToday , month , day]
		pred = model.predict(input_lst)
		output = pred
		if output == 0:
			return render_template("after_sunny.html")
		else:
			return render_template("after_rainy.html")

if __name__=='__main__':
	app.run(debug=False)