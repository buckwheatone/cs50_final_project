from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from application import login_manager
from application.models import User
from flask_login import current_user
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

class UpdateAccountForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), length(min=3, max=20, message="Username must be at least 3 characters")])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                print(user)
                raise ValidationError("Username already taken.")

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError("Email already in use.")

class UpdateProfilePic(FlaskForm):
    profile_pic = FileField('Update Profile Pic', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField("Update")

class DeleteAccountForm(FlaskForm):
    pass 

class CreateCardForm(FlaskForm): 
    card_title = StringField('Title', validators=[length(1, 300, message="Title must be under 300 characters")])
    card_question = StringField('Question', validators=[])
    card_answer = StringField('Answer', validators=[])
    card_tags = StringField('Tags', validators=[]) 
    deck_name = StringField('Deck', validators=[])
    # TODO: ability to add images, files, audio, cloze, use markdown 
    submit = SubmitField("+ Add")
