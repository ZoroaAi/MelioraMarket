import random
from flask import Blueprint, redirect ,render_template, request, flash, session, url_for
from flask_login import login_required, current_user
from . import db
from .models import Basket, User, Product, BasketItem
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html', user = current_user)  


@views.route('/basket', methods=['GET','POST'])
@login_required
def basket():
    basket = Basket.query.filter_by(user_id=current_user.id).first()
    if basket:
        basket_items = basket.basket_item
        print('Basket Items:', basket_items)
        total_items, total_price = calculate_totals(basket_items)
        return render_template('basket.html', basket_items=basket_items, total_items=total_items,total_price=total_price)
    else:
        return render_template('basket.html')

def calculate_totals(basket_items):
    total_items = 0
    total_price = 0
    for item in basket_items:
        total_items += item.quantity
        total_price += item.product.price * item.quantity
        print(f"Item: {item.product.title}, Quantity: {item.quantity} Price: {item.product.price} Current Total: {total_price}")
    print(f"Total Items: {total_items}, Total Price: {total_price}")
    return total_items, total_price

@views.route('/account', methods=['POST','GET'])
@login_required
def account():
    total_basket_items, total_basket_price = get_totals_for_user(current_user.id)
    
    profile_pics = [
        "images/profile_pic_woman.svg",
        "images/profile_pic_woman.svg",
    ]
    random_profile_pic = random.choice(profile_pics)
    
    return render_template('account.html', total_basket_items=total_basket_items, total_basket_price=total_basket_price,profile_pic=random_profile_pic)

# Get calculated totals from user
def get_totals_for_user(user_id):
    basket = Basket.query.filter_by(user_id=user_id).first()
    if basket:
        basket_item = basket.basket_item
        return calculate_totals(basket_item)
    return 0, 0

# Assign a random profile pic between male/female
def random_profile_pic():
    profile_pics = [
        "images/profile_pic_woman.svg",
        "images/profile_pic_woman.svg",
    ]
    random_profile_pic = random.choice(profile_pics)
    return random_profile_pic