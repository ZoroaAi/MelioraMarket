from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Database Models
class User(db.Model, UserMixin):
    # User info
    id = db.Column(db.Integer, primary_key=True)
    notes = db.relationship('Basket')
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    
class Product(db.Model):
    # Product info
    id = db.Column(db.Integer, primary_key = True)
    basket = db.Column(db.Integer, db.ForeignKey('user.id'))
    p_name = db.Column(db.String(150))
    p_price = db.Column(db.Float(1000))
    
class Basket(db.Model):
    # Basket info
    id = db.Column(db.Integer, primary_key = True)
    product = db.relationship('Product')