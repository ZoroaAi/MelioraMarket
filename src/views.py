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
    return render_template('account.html')