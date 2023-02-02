from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = 'database.db'

# Initialise Flask
def create_app():
    app = Flask(__name__)
    
    # Encrypting Session data and cookies
    app.config['SECRET_KEY'] = 'superSecretKey'
    app.config['SQLAlCHEMY_DATABASE_URI'] = f'sqlite://{DB_NAME}'
    db.init_app(app)
    
