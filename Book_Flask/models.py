from Book_Flask import db, login_user_manager
from flask_login import UserMixin



# it's very important to be executed "login_user" in routes.py (import from flask_login)
@login_user_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))




class User(db.Model, UserMixin):
    UserID = db.Column(db.String(10), primary_key = True)
    FirstName = db.Column(db.String(length = 20, convert_unicode = True), nullable = False)
    LastName = db.Column(db.String(length = 80, convert_unicode = True), nullable = False)
    Phone = db.Column(db.String(20))
    Email = db.Column(db.String(100), unique = True, nullable = False)
    ImgUrl = db.Column(db.String(100), nullable = False, default = 'default.jpg')
    Password = db.Column(db.String(100), nullable = False)

    def __repr__(self):
        return f"User('{self.LastName}', '{self.Email}', '{self.ImgUrl}')"

class Book(db.Model):
    BookID = db.Column(db.String(10), primary_key = True)
    Title = db.Column(db.String(length = 150, convert_unicode = True), nullable = False)
    ISBN = db.Column(db.String(13), unique = True)
    Authors = db.Column(db.String(length = 250, convert_unicode = True))
    PublicationYear = db.Column(db.Integer)
    ImgUrl = db.Column(db.String(100), default = 'default_book.jpg')
    Price = db.Column(db.Integer, default = 100000)
    Rating = db.Column(db.Integer)

# class Store(db.Model):
# 	StoreID = db.Column(db.String(10), primary_key = True, nullable = False)
# 	Phone = db.Column(db.String(20))
# 	Address = db.Column(db.String(length = 100, convert_unicode = True))
# 	ManagerID = db.Column(db.String(10), db.ForeignKey('user.UserID'), nullable = False)
# class Stock(db.Model):
# 	StoreID = db.Column(db.String(10), primary_key = True, db.ForeignKey('store.StoreID'), nullable = False)
# 	BookID = db.Column(db.String(10), primary_key = True,db.ForeignKey('book.BookID'))
# 	Quantity = db.Column(db.Integer, default = 0)
class Orders(db.Model):
    OrderID = db.Column(db.String(10), primary_key = True)
    UserID = db.Column(db.String(10), db.ForeignKey('user.UserID'), nullable = False)
    Date = db.Column(db.DateTime)
    isDelivery = db.Column(db.Boolean, default = 0)
    TotalPrice = db.Column(db.Integer)

class OrderDetails(db.Model):
    OrderID = db.Column(db.String(10), db.ForeignKey('orders.OrderID'), primary_key = True)
    BookID = db.Column(db.String(10), db.ForeignKey('book.BookID'), primary_key = True)
    Quantity = db.Column(db.Integer, default = 1)
