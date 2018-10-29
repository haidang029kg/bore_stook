from flask import Flask
from flaskext.mysql import MySQL


from Book_Flask.config import Config



db = MySQL()


def create_app(config_class = Config):
	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)

	from Book_Flask.main.routes import main
	app.register_blueprint(main)

	return app