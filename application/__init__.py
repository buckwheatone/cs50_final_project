from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'This is my secret key!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

login_manager = LoginManager(app) 
login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'
# login_manager.login_message_category = 'danger'
# LINES ABOVE: all application imports and app creation/config included here 

from application import routes
