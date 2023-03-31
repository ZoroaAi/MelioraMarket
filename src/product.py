import json
from flask import Blueprint, jsonify, redirect ,render_template, request, flash, session, url_for
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
    basket = get_or_create(Basket, user_id=current_user.id)

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

# Get or Create Pattern
def get_or_create(model, **kwargs):
    instance = model.query.filter_by(**kwargs).first()
    if not instance:
        instance = model(**kwargs)
        db.session.add(instance)
        db.session.commit()
    return instance


@product.route('/update_basket_item/<int:basket_item_id>', methods=['POST'])
@login_required
def update_basket_item_id(basket_item_id):
    new_quantity = request.form.get('quantity')
    
    try:
        new_quantity = int(new_quantity)
        if new_quantity <=0:
            raise ValueError()
    except ValueError:
        return jsonify(success=False,message="Basket item not found")
    
    basket_item = BasketItem.query.get(basket_item_id)
    if not basket_item or basket_item.basket.user_id != current_user.id:
        return jsonify(success=False, message="Basket item not found")
    
    basket_item.quantity = new_quantity
    db.session.commit()
    
    return jsonify(success=True)