from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = 'database.db'

# Initialise Flask
def create_app():
    app = Flask(__name__)
    
    # Encrypting Session data and cookies
    app.config['SECRET_KEY'] = 'superSecretKey'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    from .product import product
    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')
    app.register_blueprint(product, url_prefix = '/')
    
    with app.app_context():
        db.create_all()
        print('Created Database: %s' % DB_NAME)
    return app
    
