import json
from flask import Flask
from flask_migrate import Migrate
from .models import Product, User
from .extensions import db
from flask_login import LoginManager, current_user
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter

login_manager = LoginManager()

DB_NAME = 'database.db'

# Initialise Flask
def create_app():    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'superSecretKey'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)
    csrf = CSRFProtect(app)
    bcrypt = Bcrypt(app)
    limiter = Limiter(app)
    
    app.extensions['bcrypt'] = bcrypt
    app.extensions['limiter'] = limiter
    
    with app.app_context():
        db.create_all()
    
    from .views import views
    from .auth import auth
    from .product import product
    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')
    app.register_blueprint(product, url_prefix = '/')
        
    create_and_populate_db(app)
    
    # making the 'current_user' available in all templates
    app.context_processor(lambda:{'current_user':current_user})
    
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
        
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
