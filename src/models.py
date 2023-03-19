from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from .extensions import db

# Database Models
class User(db.Model):
    # User info
    id = db.Column(db.Integer, primary_key=True)
    # basket = db.relationship('BasketItem')
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    
    def __init__(self, email,password,firstName):
        self.email = email
        self.password = password
        self.firstName = firstName
    
    def __repr__(self) -> str:
        return super().__repr__()
    
class Product(db.Model):
    # Product info
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    img_url = db.Column(db.String(200), nullable=False)
    market_name = db.Column(db.String(100), nullable=False)
    
    def __init__(self,title,price,img_url,market_name):
        self.title = title
        self.price = price
        self.img_url = img_url
        self.market_name = market_name 
    
    def __repr__(self):
        return f"Product<'{self.market_name},{self.title}',{self.price},{self.img}>"
 
class Basket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
   
class BasketItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    basket_id = db.Column(db.Integer, db.ForeignKey('basket.id'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

