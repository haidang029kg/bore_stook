from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

import os
LOCAL_URI = 'mysql+pymysql://flask:Flask_123@127.0.0.1:3306/borestook'
LIVE_URI = 'mysql+pymysql://flask:Flask_123@localhost/borestook?unix_socket=/cloudsql/final-thesis-100496:asia-east2:borestook'

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

if os.environ.get('GAE_INSTANCE'):
    app.config['SQLALCHEMY_DATABASE_URI'] = LIVE_URI
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = LOCAL_URI

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587

app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

login_user_manager = LoginManager(app)
login_user_manager.session_protection = "strong"
login_user_manager.login_view = 'user.login' # route of login
login_user_manager.login_message_category = 'info' # bootstrap name for messgage

from Book_Flask.main.routes import main
from Book_Flask.user.routes import user
from Book_Flask.admin.routes import admin

app.register_blueprint(main)
app.register_blueprint(user)
app.register_blueprint(admin)