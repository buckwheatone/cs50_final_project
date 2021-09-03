from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField 
from wtforms.validators import DataRequired, Email, EqualTo, length

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', 
                           validators=[DataRequired(), length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), length(min=8, max=200)]) 
    submit = SubmitField("Sign Up") 

    # add username and e-mail uniqueness validations here

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), length(min=8, max=200)]) 
    remember = BooleanField("Remember me")
    submit = SubmitField("Log in") 
