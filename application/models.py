from application import db, login_manager
from datetime import datetime 
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(20), unique=True, nullable=False) 
    email = db.Column(db.String(120), unique=True, nullable=False) 
    image_file = db.Column(db.String(20), nullable=False, default='default.jpeg')
    password = db.Column(db.String(), nullable=False) 
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    active = db.Column(db.Integer, nullable=False, default=1)
    # last login?
    cards = db.relationship('Card', backref='author', lazy=True)

    def __repr__(self): 
        return f"User({self.username}, {self.email}, {self.image_file})"

class Card(db.Model): 
    id = db.Column(db.Integer, primary_key=True) 
    card_title = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    card_question = db.Column(db.Text, nullable=False) 
    card_answer = db.Column(db.Text, nullable=False) 
    last_reviewed = db.Column(db.DateTime, nullable=False) 
    next_review = db.Column(db.DateTime, nullable=False) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 

    def __repr__(self):
        return f"Card({self.card_title}-- Q:{self.card_question} A:{self.card_answer})"

class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.Text, nullable=False) 
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False) 
    card_count = db.Column(db.Integer, nullable=False)
    
    def __repr(self):
        return f"Deck({self.name}, {self.card_count} Cards)"
