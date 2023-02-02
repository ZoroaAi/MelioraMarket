from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Database Models
class User(db.Model, UserMixin):
    # User info to store
    id = db.Column(db.Integer, primary_key=True)
    notes = db.relationship('Product')
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    
class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    basket = db.Column(db.Integer, db.ForeignKey('user.id'))
    p_name = db.Column(db.String(150))
    p_price = db.Column(db.Float(1000))
    