from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from forms import RegistrationForm
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='This is my secret key!')

@app.route("/")
def index():
    return render_template("index.html") 

@app.route("/register", methods=["GET", "POST"]) 
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = generate_password_hash(form.password.data) 

        # TODO ensure username isn't taken

        # db.execute("INSERT INTO users (username, hash) VALUES(?, ?)",
        #     request.form.get("username"),
        #     generate_password_hash(request.form.get("password"))
        #     )
        return redirect("/login")
    return render_template("register.html", form=form) 

@app.route("/login", methods=["GET", "POST"])
def login():
    # need to validate: only username and password match
    
    # Forget any user_id
    # session.clear()
    
    if request.method == 'POST': #and form.validate():
        # look up username and password in db

            # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        return redirect("/dashboard") 
    
    return render_template("login.html") 

@app.route("/dashboard")
def dashboard():
    return "here's your dashboard!"


if __name__ == '__main__':
    # Note, per docs app.run is not good for production
    app.run(debug=True) 
