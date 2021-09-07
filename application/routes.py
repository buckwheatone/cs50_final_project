from flask import flash, redirect, render_template, request, session, url_for
from application import app, db
from .forms import LoginForm, RegistrationForm, UpdateAccountForm
from .models import User, Card
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, current_user, login_required

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

@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
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

@app.route("/test4")
def test4():
    return render_template("test4.html") 
    