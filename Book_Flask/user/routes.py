from flask import Blueprint, render_template, url_for, flash, redirect, request

from Book_Flask import db, bcrypt
from Book_Flask.models import User
from Book_Flask.user.forms import RegistrationForm, LoginForm

from flask_login import login_user, logout_user, current_user, login_required


user = Blueprint('user', __name__)

@user.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        user = User(email = form.email.data,
                    name = form.name.data, 
                    password = hashed_password)
        
        db.session.add(user)
        db.session.commit()
            
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('user.login'))
    
    return render_template('register.html', title = 'Register', form = form)

@user.route("/login", methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)

            next_page = request.args.get('next')
            flash('Login successful!', 'success')

            return redirect(next_page) if next_page else redirect(url_for('main.home'))

        else:
            flash('Login unsucessful! please check username and password', 'danger')
    
    return render_template('login.html', title = 'Log In', form = form)