from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Login.query.get(int(user_id))

class Login(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    user_password = db.Column(db.String(20), nullable=False)
    # posts = db.relationship('Post', backref='author', lazy=True)
    def __repr__(self):
        return f"User('{self.user_id}', '{self.username}')"

class Reviews(db.Model):
    location_id = db.Column(db.Integer,  db.ForeignKey('Locations.location_id'))
    review_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Login.user_id'), nullable=False)
    review = db.Column(db.String(300), nullable=False)
    
class Locations(db.Model):
    location_id = db.Column(db.Integer, primary_key=True)
    loc_name = db.Column(db.String(24))
    business_type = db.Column(db.String(24))
    review = db.Column(db.String(24))
    
class UserProfile(db.Model):
    profile_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Login.user_id'), nullable=False)
    first_name = db.Column(db.String(24))
    last_name = db.Column(db.String(24))
    likes = db.Column(db.String(24))
    dislikes = db.Column(db.String(24))
    
class Qual_Values(db.Model):
    location_id = db.Column(db.Integer,  db.ForeignKey('Locations.location_id'))
    score_id = db.Column(db.Integer, primary_key=True)
    quietnes = db.Column(db.Decimal)
    price = db.Column(db.Decimal)
    distance = db.Column(db.Decimal)
    food_quality = db.Column(db.Decimal)
