from flask import Blueprint ,render_template, request, flash
from flask_login import login_required, current_user
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html', user = current_user)

@views.route('/browse', methods=['GET','POST'])
def browse():
    with open('src/test_data/tesco_test.json') as json_file:
        data = json.load(json_file)
    return render_template('browse.html', data = data)

# C:\Users\saura\Desktop\Uni\Year_3\Final Year Project\MelioraMarket\src\test_data\tesco_test.json
# C:\Users\saura\Desktop\Uni\Year_3\Final Year Project\MelioraMarket\src\views.py

@views.route('/basket', methods=['GET','POST'])
def basket():
    return render_template('basket.html')