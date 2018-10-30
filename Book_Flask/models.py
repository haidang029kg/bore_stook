from Book_Flask import db, login_user_manager
from flask_login import UserMixin



# it's very important to be executed "login_user" in routes.py (import from flask_login)
@login_user_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))




class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(length = 100, convert_unicode = True), nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    image_file = db.Column(db.String(100), nullable = False, default = 'default.jpg')
    password = db.Column(db.String(100), nullable = False)
    
    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.image_file}')"