import json
from flask import Blueprint, jsonify, redirect ,render_template, request, flash, session, url_for
from flask_login import current_user, login_required, UserMixin
from . import db
from .models import Basket, User, Product, BasketItem
from flask_paginate import Pagination, get_page_args 
from flask_wtf import FlaskForm

product = Blueprint('product', __name__)

# Browse Page -- Functions: Search / Pagination --
@product.route('/browse', methods=['GET','POST'])
def browse():
    page = request.args.get('page', 1, type=int)
    per_page = 24
    query = request.args.get('title')
    price_order = request.args.get('price_order')
    markets = request.args.getlist('markets')

    products_query = Product.query

    if query:
        products_query = products_query.filter(Product.title.ilike(f'%{query}%'))

    if price_order == 'asc':
        products_query = products_query.order_by(Product.price.asc())
    elif price_order == 'desc':
        products_query = products_query.order_by(Product.price.desc())

    if markets:
        products_query = products_query.filter(Product.market_name.in_(markets))

    products = products_query.paginate(page=page, per_page=per_page, error_out=False)

    title = 'Browse'
    template = "html_components/card_template.html"
    pagination = Pagination(page=page, total=products_query.count(), per_page=per_page, css_framework='bootstrap4')
    return render_template('browse.html', data=products.items, pagination=pagination, title=title, template=template, query=query)



@product.route('/filtered-browse', methods=['GET'])
def filtered_browse():
    page = request.args.get('page', 1, type=int)
    per_page = 24
    price_order = request.args.get('price_order')

    products_query = Product.query

    if price_order == 'asc':
        products_query = products_query.order_by(Product.price.asc())
    elif price_order == 'desc':
        products_query = products_query.order_by(Product.price.desc())

    products = products_query.paginate(page=page, per_page=per_page, error_out=False)
    title = 'Filtered Browse'
    pagination = Pagination(page=page, total=products.total, per_page=per_page, css_framework='bootstrap4')
    return render_template('html_components/card_template.html', data=products.items, pagination=pagination, title=title, query=None)




# Add To Basket Function
@product.route('/add_to_basket/<int:product_id>', methods = ['POST'])
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


# Update Quantity and Remove Item from Basket
@product.route('/update_basket_item/<int:basket_item_id>', methods=['POST'])
@login_required
def update_basket_item(basket_item_id):
    action =request.form.get('action')
    
    basket_item = BasketItem.query.get(basket_item_id)
    if not basket_item or basket_item.basket.user_id != current_user.id:
        flash("Basket item not found", "danger")
        return redirect(url_for('views.basket'))

    # Change Quantity of Basket Item
    if action == "update":
        new_quantity = request.form.get('item_quantity')
        change_quantity(new_quantity)
        basket_item.quantity = new_quantity
    elif action == "remove":
        db.session.delete(basket_item)
        flash("Item removed from basket","success")
       
    db.session.commit()

    return redirect(url_for('views.basket'))


def change_quantity(new_quantity):
    if not new_quantity:
        flash("Quantity not provided", "danger")
        return redirect(url_for('product.basket'))

    try:
        new_quantity = int(new_quantity)
        flash("Quantity updated successfully", "success")
        if new_quantity <= 0:
            raise ValueError()
    except ValueError:
        flash("Invalid quantity", "danger")
        return redirect(url_for('views.basket'))
    
