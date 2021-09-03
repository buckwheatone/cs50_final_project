from flask import flash, redirect, render_template, request, session, url_for
from application import app
from .forms import LoginForm, RegistrationForm
from .models import User, Card
from werkzeug.security import check_password_hash, generate_password_hash

# remove later
cards = [
    {
        'title': 'Card 1',
        'tags': 'Programming',
        'question': 'What does import this do in the Python REPL?',
        'answer': 'Prints out the Zen of Python'
    }
]

@app.route("/")
def index():
    return render_template("index.html") 

@app.route("/register", methods=["GET", "POST"]) 
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = generate_password_hash(form.password.data) 
        flash(f"Account created for {username}!", category="success")
        
        # TODO ensure username isn't taken

        return redirect(url_for("dashboard")) 
    return render_template("register.html", form=form) 

@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    # session.clear()
    form = LoginForm() 
    if request.method == 'POST' and form.validate_on_submit():
        # look up username and password in db
        # Remember which user has logged in
        # session["user_id"] = rows[0]["id"]
        return redirect("/dashboard") 
    
    return render_template("login.html", form=form) 

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", cards=cards)

@app.route("/forgotpassword")
def forgot_password():
    pass

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