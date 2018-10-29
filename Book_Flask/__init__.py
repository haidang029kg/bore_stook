from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

import os

URI = 'mysql+mysqlconnector://' + os.environ.get('MYSQL_USER') + ':' + os.environ.get('MYSQL_PASSWORD') + '@localhost/' + os.environ.get('MYSQL_DB')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from Book_Flask.main.routes import main
from Book_Flask.user.routes import user
app.register_blueprint(main)
app.register_blueprint(user)