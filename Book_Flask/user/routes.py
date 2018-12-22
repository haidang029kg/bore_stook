from flask import Blueprint, render_template, url_for, flash, redirect, request, jsonify

from Book_Flask import db, bcrypt
from Book_Flask.models import Book, Author, Genre, Orders, OrderDetails, generate_id, Status, Paymentmethod, Ispaid
from Book_Flask.user.utilities import *
from Book_Flask.user.forms import *

import json

from flask_login import login_user, logout_user, current_user, login_required


user = Blueprint('user', __name__)


@user.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You have already logged in.', 'info')
        return redirect(url_for('main.home'))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')

        user = User(Email=form.email.data,
                    Phone=form.phone.data,
                    FirstName=form.fname.data,
                    LastName=form.lname.data,
                    Password=hashed_password)

        db.session.add(user)
        db.session.commit()
        db.session.close()

        send_token_register(user=user)

        flash('An email has been sent with an instruction to complete your registration. Please check your email to continue!!!', 'info')
        return redirect(url_for('main.home'))

    return render_template('register.html', title='Register', form=form)


@user.route("/register_token/<token>", methods=['GET', 'POST'])
def register_token(token):
    if current_user.is_authenticated:
        flash('You have already logged in.', 'info')
        return redirect(url_for('user.home'))

    user = User.verify_token(token)

    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('user.register'))

    else:
        flash('Register completely!!! Now you can login', 'info')
        return redirect(url_for('user.login'))

    return redirect(url_for('user.register'))


@user.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(Email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.Password, form.password.data):
            login_user(user, remember=form.remember.data)

            next_page = request.args.get('next')
            flash('Login successful!', 'success')

            return redirect(next_page) if next_page else redirect(url_for('main.home'))

        else:
            flash('Login unsucessful! please check username and password', 'danger')

    return render_template('login.html', title='Log In', form=form)


@user.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@user.route("/request_passwd", methods=['GET', 'POST'])
def request_passwd():
    if current_user.is_authenticated:
        flash('you have already logged in!!!', 'info')
        return redirect(url_for('main.home'))

    form = RequestPasswdForm()

    if form.validate_on_submit():
        user = User.query.filter_by(Email=form.email.data).first()

        send_token_reset(user)

        flash('An email has been sent with an instruction to reset your password', 'info')

        return redirect(url_for('user.login'))

    return render_template('request_password.html', title='Password Reset Request', form=form)


@user.route("/reset_passwd/<token>", methods=['GET', 'POST'])
def reset_passwd(token):
    if current_user.is_authenticated:
        return redirect(url_for('user.home'))

    user = User.verify_token(token)

    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('user.request_passwd'))

    form = ResetPasswdForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.Password = hashed_password

        db.session.commit()
        flash('Your password has been updated! Login now...', 'success')

        return redirect(url_for('user.login'))

    return render_template('reset_password.html', title='Reset Password', form=form)


@user.route("/user/change_password", methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswdForm()
    user = User.query.get(current_user.get_id())

    if form.validate_on_submit():

        if not(bcrypt.check_password_hash(user.Password, form.current_password.data)):

            flash('Current password is incorrect', 'warning')
            logout_user()

            return redirect(url_for('user.login', form=form, title='Change Password'))

        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.Password = hashed_password

        db.session.commit()
        db.session.close()

        flash('Changed password completely!', 'info')

        login_form = LoginForm()
        return redirect(url_for('user.login', form=login_form, title='Login'))

    return render_template('change_password.html', title='Change Password', form=form)


@user.route("/user/account", methods=['GET', 'POST'])
@login_required
def account():
    form = AccountForm()

    if form.validate_on_submit():

        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.ImgUrl = picture_file

        current_user.FirstName = form.fname.data
        current_user.LastName = form.lname.data
        current_user.Phone = form.phone.data

        db.session.commit()
        flash('Your account has been updated!', 'info')

        return redirect(url_for('user.account', title='Account', form=form))

    elif request.method == 'GET':
        form.fname.data = current_user.FirstName
        form.lname.data = current_user.LastName
        form.phone.data = current_user.Phone

    image_file = url_for(
        'static', filename='image/profile_user_pic/' + str(current_user.ImgUrl))

    return render_template('account.html', form=form, title='Account', image_file=image_file)


@user.route("/create_order", methods=['POST'])
@login_required
def create_order():
    order = request.form.getlist('order')[0]
    order = json.loads(order)

    order_detail = order['Detail']

    order_detail = json.loads(order_detail)

    order_id = generate_id('order')
    user_id = current_user.get_id()

    data_order = Orders(OrderID=order_id,
                        UserID=user_id,
                        Address=order.get('Address'),
                        Phone=order.get('Phone'),
                        TotalPrice=order.get('TotalPrice'),
                        IsPaid=order.get('IsPaid'),
                        Status=order.get('Status'),
                        PaymentMethod=order.get('PaymentMethod'))

    data_order_details = []

    for i in order_detail:
        each_detail = OrderDetails(OrderID=order_id,
                                   BookID=i.get('BookID'),
                                   Quantity=i.get('Quantity'))
        data_order_details.append(each_detail)

    if (data_order):
        if (data_order_details):
            db.session.add(data_order)

            for i in data_order_details:
                db.session.add(i)

        db.session.commit()
        db.session.close()
        flash('Ordered successfully!!!', 'info')

    return jsonify({'success': 'done!'})


@user.route("/user/ordered_history")
@login_required
def ordered_history():

    page = request.args.get('page', 1, type=int)
    per_page = 5

    id_user = current_user.get_id()

    items = db.session.query(Orders.OrderID, Orders.Date, Orders.Address, Orders.Phone, Orders.TotalPrice, Ispaid.NamePaid, Paymentmethod.NamePayment, Status.NameStatus).filter(Orders.UserID == id_user).filter(
        Orders.IsPaid == Ispaid.IsPaidID).filter(Orders.PaymentMethod == Paymentmethod.PaymentMethodID).filter(Orders.Status == Status.StatusID).order_by(Orders.Date.desc()).paginate(page = page, per_page = per_page)

    db.session.close()

    return render_template('ordered_history.html', title='Ordered History', items=items)


@user.route("/ordered_detail", methods = ['GET'])
@login_required
def ordered_detail():
    ordered_id = request.args.get('ordered_id')

    items = db.session.query(Book.ImgUrl, Book.Title, Book.Price, OrderDetails.Quantity).filter(OrderDetails.OrderID == ordered_id).filter(OrderDetails.OrderID == Orders.OrderID).filter(OrderDetails.BookID == Book.BookID).all()
    total_price = db.session.query(Orders.TotalPrice).filter(Orders.OrderID == ordered_id).first()[0]

    db.session.close()

    return jsonify({
        'ordered_id' : ordered_id,
        'total_price' : total_price,
        'items' : items
    })