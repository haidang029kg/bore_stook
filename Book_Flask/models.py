from Book_Flask import db, login_user_manager, app
from flask_login import UserMixin
from datetime import datetime
import uuid

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer



# it's very important to be executed "login_user" in routes.py (import from flask_login)
@login_user_manager.user_loader
def user_loader(user_id):
    return User.query.get(str(user_id))


def generate_id(type):
    id = str(uuid.uuid1())

    switcher = {
        'user' : str('user-' + id)[:16],
        'book' : str('book-' + id),
        'order' : str('order-' + id)[:16]
    }
    return switcher.get(type)


class User(db.Model, UserMixin):
    UserID = db.Column(db.Integer, primary_key = True)
    FirstName = db.Column(db.String(length = 50, convert_unicode = True), nullable = False)
    LastName = db.Column(db.String(length = 50, convert_unicode = True), nullable = False)
    Phone = db.Column(db.String(15))
    Email = db.Column(db.String(100), unique = True, nullable = False)
    ImgUrl = db.Column(db.String(100), nullable = False, default = 'default.jpg')
    Password = db.Column(db.String(100), nullable = False)
    

    # default is to return id attribute, but in this case is UserID attribute
    # override this def, bc it's executed in user_login from flask_login     
    def get_id(self):
        return self.UserID

        

    def get_token(self, expires_sec = 1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)

        return s.dumps({'user_id': self.UserID}).decode('utf-8')

    @staticmethod
    def verify_token(token):
        s = Serializer(app.config['SECRET_KEY'])

        try: #return user id
            user_id = s.loads(token)['user_id']
        except:
            return None
            
        return User.query.filter_by(UserID = user_id).first()



class Book(db.Model):
    BookID = db.Column(db.Integer, primary_key = True)
    Title = db.Column(db.Text(convert_unicode = True), nullable = False)
    ISBN = db.Column(db.String(13), unique = True)
    AuthorsID = db.Column(db.Text(convert_unicode = True))
    PublicationYear = db.Column(db.Integer)
    ImgUrl = db.Column(db.String(100), default = 'default_book.jpg')
    Price = db.Column(db.Float, default = 100)
    AvgRating = db.Column(db.Float)
    Quantity = db.Column(db.Integer, default = 0)
    GenreID = db.Column(db.Integer, db.ForeignKey('genre.GenreID'), nullable = False)


class Genre(db.Model):
    GenreID = db.Column(db.Integer, primary_key = True)
    Name = db.Column(db.String(length = 100, convert_unicode = True), nullable = False)


class Author(db.Model):
    AuthorID = db.Column(db.Integer, primary_key = True)
    Name = db.Column(db.String(length = 250, convert_unicode = True))



class Orders(db.Model):
    OrderID = db.Column(db.String(length = 16, convert_unicode = True), primary_key = True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'), nullable = False)
    Date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow())
    Address = db.Column(db.Text(convert_unicode = True), nullable = False)
    TotalPrice = db.Column(db.Float ,nullable = False)
    IsPaid = db.Column(db.Boolean, default = 0)
    # 0. No
    # 1. Yes
    Status = db.Column(db.Integer, default = 0)
    # 0. Waiting
    # 1. Packaging
    # 2. Delivering
    # 3. Delivered
    PaymentMethod = db.Column(db.Integer, default = 0)
    # 0. Credit Card
    # 1. Cash
    # 2. Bank Transfer
    # 3. Code


class OrderDetails(db.Model):
    OrderID = db.Column(db.String(length = 16, convert_unicode = True), primary_key = True)
    BookID = db.Column(db.Integer, db.ForeignKey('book.BookID'), primary_key = True)
    Quantity = db.Column(db.Integer, default = 1)