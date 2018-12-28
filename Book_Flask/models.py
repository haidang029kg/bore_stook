from Book_Flask import db, login_user_manager, app
from flask_login import UserMixin, current_user
from datetime import datetime
import uuid
from flask import flash, redirect, url_for, request

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from functools import wraps

# it's very important to be executed "login_user" in routes.py (import from flask_login)


@login_user_manager.user_loader
def user_loader(user_id):
    user = User.query.get(str(user_id))
    return user


# decoration admin_login_required
def admin_login_required(f):
    @wraps(f)
    def decoration_admin_required(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('admin.login', next=request.url))
        else:
            if not current_user.is_admin:
                return redirect(url_for('admin.login', next=request.url))
        return f(*args, **kwargs)
    return decoration_admin_required


def generate_id(type):
    id = str(uuid.uuid1())

    switcher = {
        'user': str('user-' + id)[:16],
        'book': str('book-' + id),
        'order': str('order-' + id)[:16]
    }
    return switcher.get(type)


class User(db.Model, UserMixin):
    UserID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(
        db.String(length=50, convert_unicode=True), nullable=False)
    LastName = db.Column(
        db.String(length=50, convert_unicode=True), nullable=False)
    Phone = db.Column(db.String(15), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    ImgUrl = db.Column(db.String(100), nullable=False, default='default.jpg')
    Password = db.Column(db.String(100), nullable=False)
    RoleAdmin = db.Column(db.Boolean(), nullable=False, default=False)

    # default is to return id attribute (inherit from UserMixin), but in this case is UserID attribute
    # override this def from UserMixin, bc it's executed in user_login from flask_login

    def get_id(self):
        return self.UserID

    def get_fullname(self):
        return (self.FirstName + ' ' + self.LastName)

    @property
    def is_admin(self):
        return self.RoleAdmin

    def get_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)

        return s.dumps({'user_id': self.UserID}).decode('utf-8')

    @staticmethod
    def verify_token(token):
        s = Serializer(app.config['SECRET_KEY'])

        try:  # return user id
            user_id = s.loads(token)['user_id']
        except:
            return None

        return User.query.filter_by(UserID=user_id).first()


class Book(db.Model):
    BookID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.Text(convert_unicode=True), nullable=False)
    ISBN = db.Column(db.String(13), unique=True)
    AuthorsID = db.Column(db.Text(convert_unicode=True))
    PublicationYear = db.Column(db.Integer)
    ImgUrl = db.Column(db.String(100), default='default_book.jpg')
    Price = db.Column(db.Float, default=100)
    AvgRating = db.Column(db.Float)
    Quantity = db.Column(db.Integer, default=0)
    GenreID = db.Column(db.Integer, db.ForeignKey(
        'genre.GenreID'), nullable=False)


class Genre(db.Model):
    GenreID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(
        db.String(length=100, convert_unicode=True), nullable=False)


class Author(db.Model):
    AuthorID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(length=250, convert_unicode=True))

    def getAuthorID(self):
        return self.AuthorID



class Orders(db.Model):
    OrderID = db.Column(
        db.String(length=16, convert_unicode=True), primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey(
        'user.UserID'), nullable=False)
    Date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    Address = db.Column(db.Text(convert_unicode=True), nullable=False)
    Phone = db.Column(db.String(15), nullable=False)
    TotalPrice = db.Column(db.Float, nullable=False)
    IsPaid = db.Column(db.SmallInteger, db.ForeignKey('ispaid.IsPaidID'))
    # 1. No
    # 2. Yes
    Status = db.Column(db.SmallInteger, db.ForeignKey('status.StatusID'))
    # 1. Waiting
    # 2. Packaging
    # 3. Delivering
    # 4. Delivered
    # 5. Rejected
    PaymentMethod = db.Column(db.SmallInteger, db.ForeignKey(
        'paymentmethod.PaymentMethodID'))
    # 1. Credit Card
    # 2. Cash
    # 3. Bank Transfer
    # 4. Code


class OrderDetails(db.Model):
    OrderID = db.Column(
        db.String(length=16, convert_unicode=True), primary_key=True)
    BookID = db.Column(db.Integer, db.ForeignKey(
        'book.BookID'), primary_key=True)
    Quantity = db.Column(db.Integer, default=1)


class Ispaid(db.Model):
    IsPaidID = db.Column(db.SmallInteger, primary_key=True)
    NamePaid = db.Column(
        db.String(length=5, convert_unicode=True), nullable=False)


class Status(db.Model):
    StatusID = db.Column(db.SmallInteger, primary_key=True)
    NameStatus = db.Column(
        db.String(length=12, convert_unicode=True), nullable=False)


class Paymentmethod(db.Model):
    PaymentMethodID = db.Column(db.SmallInteger, primary_key=True)
    NamePayment = db.Column(
        db.String(length=20, convert_unicode=True), nullable=False)


class Rules(db.Model):
    RID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Antecendents = db.Column(db.Text(convert_unicode=True), nullable=False)
    Consequents = db.Column(db.Text(convert_unicode=True), nullable=False)
    Confidence = db.Column(db.Float)


# class Admin(db.Model, UserMixin):
#     AdminID = db.Column(db.Integer, primary_key = True, autoincrement=True)
#     Email = db.Column(db.String(100), unique=True, nullable=False)
#     Password = db.Column(db.String(length=100, convert_unicode=True))

#     @property
#     def is_admin(self):
#         return True

#     def get_id(self):
#         return self.AdminID