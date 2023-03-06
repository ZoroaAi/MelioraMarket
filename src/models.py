from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm

db = SQLAlchemy()

# Database Models
class User(db.Model):
    # User info
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    baskets = db.relationship('Basket', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.email}', '{self.firstName}')"

class Product(db.Model):
    # Product info
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    img_url = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"Product<'{self.title}',{self.price},{self.img_url}>"

class Basket(db.Model):
    # Basket
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    items = db.relationship('BasketItem', backref='basket', lazy=True)

class BasketItem(db.Model):
    # Basket Info
    id = db.Column(db.Integer, primary_key=True)
    basket_id = db.Column(db.Integer, db.ForeignKey('basket.id'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f"BasketItem<'{self.product_id}',{self.quantity}>"

