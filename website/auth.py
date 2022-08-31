from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from verify_email import verify_email
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password is Incorrect!', category='error')
        else:
            flash('Email does not exists!', category='error')

    return render_template('login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        password_exemple = 'Bntm124@'
        numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:
            flash('Email already exists!', category='error')
        elif username_exists:
            flash('Username already used!', category='error')
        elif password1 != password2:
            flash('Password does not match!', category='error')
        elif len(username) < 2:
            flash('Username too short!', category='error')
        elif len(password1) < 8:
            flash('Week password, try some like: ' + password_exemple, category='error')
        elif verify_email(email) == False:
            flash('Email not valid!', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created!')
            return redirect(url_for('views.home'))
        
    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))