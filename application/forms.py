from flask_wtf import FlaskForm
from application import login_manager
from application.models import User
from wtforms import BooleanField, PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, length

@login_manager.user_loader 
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(),
                             length(min=8, max=200, message="Reminder: password must be at least 8 characters."), 
                             ])
    remember = BooleanField("Remember me")
    submit = SubmitField("Log in") 

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), length(min=3, max=20, message="Username must be at least 3 characters")])
    password = PasswordField('Password', validators=[DataRequired(), length(min=8, max=200, message="Password must be at least 8 characters")]) 
    submit = SubmitField("Sign Up") 

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            print(user)
            raise ValidationError("Username already taken.")

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("Email already in use.")
