import json
from flask import Blueprint, redirect ,render_template, request, flash, session, url_for
from flask_login import current_user, login_required, UserMixin
from . import db
from .models import Basket, User, Product, BasketItem
from flask_paginate import Pagination, get_page_args 

product = Blueprint('product', __name__)

with open('src/scraped_data/total_data.json') as json_file:
        data = json.load(json_file)

# Browse Page -- Functions: Search / Pagination --
@product.route('/browse', methods=['GET','POST'])
def browse():
    page = request.args.get('page', 1, type=int)
    per_page = 24
    start = (page-1)*per_page
    end = start+per_page
    query = request.args.get('title')
    if query:
        products = Product.query.filter(Product.title.ilike(f'%{query}%')).paginate(page=page, per_page=per_page, error_out=False)
        title = f"Search Results for '{query}'"
    else:
        products = Product.query.paginate(page=page, per_page=per_page, error_out=False)
        title = 'Browse'
    template = "html_components/card_template.html"
    pagination = Pagination(page=page, total=products.total, per_page=per_page, css_framework='bootstrap4')
    return render_template('browse.html', data=products.items, pagination=pagination, title=title, template=template, query=query)


# Return list of products on current page
def get_products_for_page(page, per_page):
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    return data[start_idx:end_idx]


# Add To Basket Function
@product.route('/add_to_basket/int:<product_id>', methods = ['POST'])
@login_required
def add_to_basket(product_id):
    # Get or create the current user's basket
    basket = Basket.query.filter_by(user_id=current_user.id).first()
    if not basket:
        basket = Basket(user_id=current_user.id)
        db.session.add(basket)
        db.session.commit()

    # Check if the product is already in the basket
    basket_item = BasketItem.query.filter_by(basket_id=basket.id, product_id=product_id).first()
    if basket_item:
        # Increment the quantity of the existing product in the basket
        basket_item.quantity += 1
    else:
        # Add the new product to the basket
        basket_item = BasketItem(basket_id=basket.id, product_id=product_id, quantity=1)
        db.session.add(basket_item)

    db.session.commit()
    flash('Product added to the basket!', 'success')
    return redirect(url_for('product.browse'))

# Display Basket
@product.route('/basket')
def display_basket():
    basket = Basket.query.filter_by(user_id=current_user.id).first()
    if basket:
        basket_items = BasketItem.query.filter_by(basket_id=basket.id).all()
    else:
        basket_items = []
    return render_template('basket.html', basket_items=basket_items)