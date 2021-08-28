from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField 
from wtforms.validators import DataRequired, Email, EqualTo, length

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('username', validators=[DataRequired(), length(min=3)])
    password = PasswordField('Password', validators=[DataRequired(), length(
                             min=8, 
                             max=200, 
                             message="Password must be at least 8 characters"
                             ),
                             EqualTo('confpass', message='Passwords must match')]) 
    confpass = PasswordField('Confpass', validators=[DataRequired(), length(
                             min=8, 
                             max=200,
                         )])
    submit = SubmitField("Submit") 

    # add username and e-mail uniqueness validations here
