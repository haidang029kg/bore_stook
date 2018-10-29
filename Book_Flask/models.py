from Book_Flask import db
from flask_login import UserMixin


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable = False)
    email = db.Column(db.String(20), unique = True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default = 'default.jpg')
    password = db.Column(db.String(60), nullable = False)
    
    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.image_file}')"