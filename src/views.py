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
        return render_template('basket.html', basket_items=basket_items)
    else:
        return render_template('basket.html')