from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
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

@auth.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # Get the form data
        email_input = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        # Validate the form data
        if User.query.filter_by(email=email_input).first():
            flash('Email already exists.', category='error')
        elif len(email_input) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # Add the new user to the database
            new_user = User(email=email_input, firstName=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account has been created!', category='success')
            return redirect(url_for('auth.login'))
    return render_template('register.html', user=current_user)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.home'))


