import os
import secrets
from application import app, db
from .forms import LoginForm, RegistrationForm, UpdateAccountForm, UpdateProfilePic
from .models import User, Card
from flask import flash, redirect, render_template, request, session, url_for
from flask_login import login_user, logout_user, current_user, login_required
from PIL import Image
from werkzeug.security import check_password_hash, generate_password_hash

# remove later
# cards = [
#     {
#         'title': 'Card 1',
#         'tags': 'Programming',
#         'question': 'What does import this do in the Python REPL?',
#         'answer': 'Prints out the Zen of Python'
#     }
# ]

@app.route("/dashboard")
@login_required
def dashboard():
    cards = Card.query.filter_by(user_id=current_user.id)
    return render_template("dashboard.html", cards=cards)

@app.route("/forgotpassword")
def forgot_password():
    pass

@app.route("/")
def index():
    return render_template("index.html") 


@app.route("/login", methods=["GET", "POST"])
def login():
    # TODO: Forget any user_id, session.clear()
    if current_user.is_authenticated: 
        return redirect(url_for('dashboard'))

    form = LoginForm() 
    if request.method == 'POST' and form.validate_on_submit():
        # TODO: session data, checking username availability
        hashed_pass = generate_password_hash(form.password.data)
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(hashed_pass, form.password.data): 
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next') 
            flash("Logged in!", category='success') 
            return redirect(next_page) if next_page else redirect(url_for('dashboard')) 
        else:
            flash("Username and password incorrect", category='danger') 
    
    return render_template("login.html", form=form) 

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login")

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    profile_pic_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(profile_pic_size)
    i.save(picture_path)
    #TODO: Consider writing clean-up actions to remove old photos

    return picture_fn

@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfilePic()
    if form.validate_on_submit():
        if form.profile_pic.data:
            picture_file = save_picture(form.profile_pic.data) 
            current_user.image_file = picture_file  
            pass 
        db.session.commit()
        # flash("Your profile pic has been updated", category="success") 
        return redirect(url_for('profile'))
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file) 
    return render_template("profile.html", image_file=image_file, form=form)
 

@app.route("/register", methods=["GET", "POST"]) 
def register():
    if current_user.is_authenticated: 
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        # TODO ensure username isn't taken
        
        hashed_pass = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, 
                    password=hashed_pass)
        db.session.add(user) 
        db.session.commit() 
        flash(f"Account created for {form.username.data}!", category="success")
        

        return redirect(url_for("login")) 
    return render_template("register.html", form=form) 

@app.route("/test", methods=['GET', 'POST']) 
def test():
    form = RegistrationForm() 
    if request.method == 'POST' and form.validate_on_submit():
        return redirect("/dashboard") 
    return render_template("test.html", form=form)

@app.route("/test2", methods=['GET', 'POST']) 
def test2():
    form = LoginForm() 
    return render_template("test2.html", form=form)

@app.route("/test3")
def test3():
    return render_template("test3.html")

@app.route("/test4", methods=['GET', 'POST'])
def test4():
    return render_template("test4.html", current_user=current_user) 
    
@app.route("/delete", methods=['get','post'])
def delete():
    return render_template("delete.html") 