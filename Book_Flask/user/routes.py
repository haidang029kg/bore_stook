from flask import Blueprint, render_template, url_for, flash, redirect, request

from Book_Flask import db, bcrypt
from Book_Flask.models import User
from Book_Flask.user.utilities import send_token_reset, send_token_register, generate_id
from Book_Flask.user.forms import RegistrationForm, LoginForm , RequestPasswdForm, ResetPasswdForm

from flask_login import login_user, logout_user, current_user, login_required


user = Blueprint('user', __name__)




@user.route("/home")
def home():
    return render_template('home.html', title = 'Home')



@user.route("/register", methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You have already logged in.', 'info')
        return redirect(url_for('main.home'))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        user = User(UserID = generate_id(type = 'user'),
                    Email = form.email.data,
                    FirstName = form.fname.data,
                    LastName = form.lname.data,
                    Password = hashed_password)

        db.session.add(user)
        db.session.commit()
        
        send_token_register(user = user)        

        flash('Un email has been sent with un instruction to complete your registration. Please check your email to continue!!!', 'info')
        return redirect(url_for('main.home'))
    
    return render_template('register.html', title = 'Register', form = form)



@user.route("/register_token/<token>", methods = ['GET', 'POST'])
def register_token(token):
    if current_user.is_authenticated:
        flash('You have already logged in.', 'info')
        return redirect(url_for('user.home'))

    user = User.verify_token(token)

    if user is None:
        flash('That is an invalid or expired token', 'warning')

        return redirect(url_for('user.register'))

    flash('Register completely!!! Now you can login', 'info')
    
    form = LoginForm()
    
    return render_template('login.html', form = form, title = 'Home')



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



@user.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))



@user.route("/request_passwd", methods = ['GET', 'POST'])
def request_passwd():
    if current_user.is_authenticated:
        flash('you have already logged in!!!', 'info')
        return redirect(url_for('main.home'))

    form = RequestPasswdForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()

        send_token_email(user)

        flash('Un email has been sent with un instruction to reset your password', 'info')

        return redirect(url_for('user.login'))

    return render_template('request_password.html', title = 'Password Reset Request', form = form)



@user.route("/reset_passwd/<token>", methods = ['GET', 'POST'])
def reset_passwd(token):
    if current_user.is_authenticated:
        return redirect(url_for('user.home'))

    user = User.verify_token(token)

    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('user.request_passwd'))
    
    form = ResetPasswdForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password

        db.session.commit()
        flash('Your password has been updated! Login now...', 'success')

        return redirect(url_for('user.login'))
    
    return render_template('reset_password.html', title = 'Reset Password', form = form)