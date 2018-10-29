from flask import render_template, request, Blueprint



main = Blueprint('main', __name__)



@main.route("/")
@main.route("/home")
def home():
	return render_template('home.html', title = 'Home page')
	#return "<h1>Home Page</h1>"