from flask import flash, redirect, render_template, request, session, url_for
from application import app, db
from .forms import LoginForm, RegistrationForm
from .models import User, Card
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, current_user

# remove later
cards = [
    {
        'title': 'Card 1',
        'tags': 'Programming',
        'question': 'What does import this do in the Python REPL?',
        'answer': 'Prints out the Zen of Python'
    }
]

@app.route("/dashboard")
def dashboard():
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
    form = LoginForm() 
    if request.method == 'POST' and form.validate_on_submit():
        # TODO: session data, checking username availability
        hashed_pass = generate_password_hash(form.password.data)
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(hashed_pass, form.password.data): 
            login_user(user, remember=form.remember.data) 
            flash("Logged in!", category='success') 
            return redirect("/dashboard") 
        else:
            flash("Username and password incorrect", category='danger') 
    
    return render_template("login.html", form=form) 

@app.route("/register", methods=["GET", "POST"]) 
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        # TODO ensure username isn't taken
        
        hashed_pass = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, 
                    password=hashed_pass)
        db.session.add(user) 
        db.session.commit() 
        flash(f"Account created for {form.username.data}!", category="success")
        

        return redirect(url_for("dashboard")) 
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

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login")
