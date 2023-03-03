from flask import Blueprint, redirect ,render_template, request, flash, session, url_for
from flask_login import login_required, current_user
from . import db
from .models import Basket, User, Product, BasketItem
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html', user = current_user)  


@views.route('/basket', methods=['GET','POST'])
def basket():
    return render_template('basket.html')