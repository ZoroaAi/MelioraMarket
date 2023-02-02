from flask import Blueprint ,render_template, request, flash
from flask_login import login_required, current_user
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html', user = current_user)

@views.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.html', user = current_user)

@views.route('/browse', methods=['GET','POST'])
def browse():
    return render_template('browse.html', user = current_user)

@views.route('/basket', methods=['GET','POST'])
def basket():
    return render_template('basket.html', user = current_user)
