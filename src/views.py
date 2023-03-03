from flask import Blueprint, redirect ,render_template, request, flash, session, url_for
from flask_login import login_required, current_user
from . import db
from .models import Basket, User, Product, BasketItem
import json

views = Blueprint('views', __name__)

with open('src/scraped_data/final_tesco_data.json') as json_file:
        data = json.load(json_file)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html', user = current_user)

@views.route('/browse', methods=['GET','POST'])
def browse():
    return render_template('browse.html', data = data)

@views.route('/add_to_basket', methods = ['POST'])
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

@views.route('/search', methods=['POST'])
def search():
    query = request.args.get('title')
    results = filter(lambda x: query.lower() in x['product_name'].lower(), data)
    return render_template('card_template.html', results=results)
    
def search_items():
    # Get the search query from the user input
    query = request.args.get('query')

    # Query the Product model for items that match the search query
    results = Product.query.filter(
        (Product.title.contains(query)) |
        (Product.category.contains(query)) |
        (Product.price.contains(query))
        (Product.quantity.contains(query))
        (Product.image.contains(query))
    ).all() 
    # Rendering the matching items
    render_template('card_template.html',results= results)
        

@views.route('/basket', methods=['GET','POST'])
def basket():
    return render_template('basket.html')

def getProductItem():
    itemId = Product.id
    productName = Product.name
    productName = BasketItem(product_id = itemId)
    db.session.add(Product)
    db.session.commit()
    