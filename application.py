from datetime import datetime 
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
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



app = Flask(__name__)
app.config['SECRET_KEY'] = 'This is my secret key!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(20), unique=True, nullable=False) 
    email = db.Column(db.String(120), unique=True, nullable=False) 
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(), nullable=False) 
    cards = db.relationship('Card', backref='author', lazy=True)

    def __repr__(self): 
        return f"User('{self.username}', '{self.email}', '{self.image_file}'')"

class Card(db.Model): 
    id = db.Column(db.Integer, primary_key=True) 
    card_title = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    card_question = db.Column(db.Text, nullable=False) 
    card_answer = db.Column(db.Text, nullable=False) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 

    def __repr__(self):
        return f"Card('{self.card_title}'-- Q:'{self.card_question}' A:'{self.card_answer}')"
    

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




if __name__ == '__main__':
    # Note, per docs app.run is not good for production
    app.run(debug=True) 

