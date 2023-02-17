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
    return render_template('browse.html', data = data, addToBasket = addToBasket)
def addToBasket():
    if request.method == 'POST':
        # Get Product from HTML
        # name = 
        image = request.form.get('image')
        price = request.form.get('price')
        quant = request.form.get('quantity')
        
        new_item = Product(img=image,price=price,quantity=quant)
        # Add Product to Database
        db.session.add(new_item)
        db.session.commit(new_item)
        
        

@views.route('/basket', methods=['GET','POST'])
def basket():
    return render_template('basket.html')

def getProductItem():
    itemId = Product.id
    productName = Product.name
    productName = BasketItem(product_id = itemId)
    db.session.add(Product)
    db.session.commit()
    