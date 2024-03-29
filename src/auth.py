import re
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method.lower() == 'post':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category="success")
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password, Try Again', category='Error')
    return render_template('/login.html', user=current_user)

# Email & Password validation regex
email_regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
password_regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    # Form Validation
    if request.method.lower() == 'post':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()
        if not email_regex.match(email):
            flash('Invalid email address', category='Error')
        elif user:
            flash('Email is already in use', category='Error')
        elif len(email)<7:
            flash('Email must be longer than 7 characters', category='Error')
        elif len(firstName) < 2:
            flash('First Name must be longer than 2 characters', category='Error')
        elif password1 != password2:
            flash('Passwords does not match', category='Error')
        elif not password_regex.match(password1):
            flash('Password must be at least 8 characters, contain one uppercase letter, one lowercase letter, one digit and one special character', category='Error')
        else:
            # Adding user to database:
            new_user = User(email=email, firstName=firstName, password = generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember= True)
            flash('Account has been created!', category='Success')
            return redirect(url_for('views.home'))
        
    return render_template('sign-up.html', user= current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))


