import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .models import Product
from .extensions import db

DB_NAME = 'database.db'

# Initialise Flask
def create_app():    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'superSecretKey'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    migrate = Migrate(app, db)
    
    with app.app_context():
        db.create_all()
    
    from .views import views
    from .auth import auth
    from .product import product
    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')
    app.register_blueprint(product, url_prefix = '/')
    
    create_and_populate_db(app)
    return app
    
def create_and_populate_db(app):
    with app.app_context():
        db.create_all()
        db.session.commit()
        print('Created Database: %s' % DB_NAME)
        add_products_from_json(app)

# Populate Database
def add_products_from_json(app):
    with app.app_context():
        with open('src/scraped_data/total_data.json', 'r') as f:
            products = json.load(f)
        for product in products:
            p = Product(title=product['title'], price = product['price'],img_url=product['img_url'], market_name=product['market'])
            db.session.add(p)
        db.session.commit()