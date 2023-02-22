from flask import Blueprint ,render_template, request, flash
from flask_login import login_required, current_user
from . import db
from .models import User, Product, BasketItem
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html', user = current_user)

@views.route('/browse', methods=['GET','POST'])
def browse():
    with open('src/test_data/tesco_test.json') as json_file:
        data = json.load(json_file)
    
    for item in data:
        new_item = Product(title = item['title'], price = item['unit_price'], img = item['image'], category = item['category'])
        db.session.add(new_item)
    db.session.commit()
    
        
    return render_template('browse.html', data = data)
  
@views.route('/search', methods=['POST'])
def search():
    query = request.args.get('title')
    matching_items = search_items(query)
    return render_template('card_template.html', query=query,matching_items=matching_items)
    
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
    