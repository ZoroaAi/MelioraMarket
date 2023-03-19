import json
import math
from flask import Blueprint, redirect ,render_template, request, flash, session, url_for
from . import db
from .models import Basket, User, Product, BasketItem
from flask_paginate import Pagination, get_page_args 

product = Blueprint('product', __name__)

with open('src/scraped_data/total_data.json') as json_file:
        data = json.load(json_file)

@product.route('/browse', methods=['GET','POST'])
def browse():
    page = request.args.get('page', 1, type=int)
    per_page = 24
    start = (page-1)*per_page
    end = start+per_page
    query = request.args.get('title')
    if query:
        # results = filter(lambda x: query.lower() in x['title'].lower(), data)
        # products = list(results)[start:end]
        # template = "html_components/card_template.html"
        # title = f"Search Results for '{query}'"
        products = Product.query.filter(Product.title.ilike(f'%{query}%')).paginate(page, per_page, error_out=False)
    else:
        # products = data[start:end]
        # template = "html_components/card_template.html"
        # title = "Browse"
        products = Product.query.paginate(page, per_page, error_out = False)
        title = 'Browse'
    template = "html_components/card_template.html"
    pagination = Pagination(page=page, total=len(data), per_page=per_page, css_framework='bootstrap4')
    return render_template('browse.html', data=products.items, pagination=pagination, title=title, template=template, query=query)


# Return list of products on current page
def get_products_for_page(page, per_page):
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    return data[start_idx:end_idx]

@product.route('/add_to_basket', methods = ['POST'])
def add_to_basket():
    product_id = request.form.get('product_id')
    if 'user_id' in session:
        user_id = session['user_id']
    
    # Add the product to he user's basket
    basket = get_basket_for_user(user_id)
    add_product(basket, product_id)
    return redirect(url_for('browse.html'))

def get_basket_for_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return None
    basket = Basket.query.filter_by(user_id=user.id).order_by(Basket.created_at.desc()).first()
    if basket is None:
        basket = Basket(user_id=user.id)
        db.session.add(basket)
        db.session.commit()
    return basket

def add_product(basket, product_id):
    # Adds given product to the basket
    item = BasketItem.query.filter_by(basket_id=basket.id, product_id=product_id).first()
    if item is None:
        # Add the product if not already in the basket
        item = BasketItem(basket_id=basket.id, product_id=product_id)
        db.session.add(item)
    else:
        item.quantity += 1
    db.session.commit()
