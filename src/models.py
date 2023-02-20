from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length

# Database Models
class User(db.Model, UserMixin):
    # User info
    id = db.Column(db.Integer, primary_key=True)
    basket = db.relationship('Basket')
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    
class Product(db.Model):
    # Product info
    id = db.Column(db.Integer, primary_key = True)
    basket = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(150))
    price = db.Column(db.Float(1000))
    img = db.Column(db.String(120), unique = True)
    quantity = db.Column(db.Integer)
    
class BasketItem(db.Model):
    # Basket info
    id = db.Column(db.Integer, primary_key = True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))


# Forms
class SearchedItems(FlaskForm):
    searched = StringField("searched", validator=[DataRequired()])
    submit = SubmitField()