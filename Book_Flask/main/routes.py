from flask import render_template, request, Blueprint
from Book_Flask.models import Book

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
	page = request.args.get('page', 1, type = int)
	per_page = 20

	items = Book.query.order_by(Book.Title.asc()).paginate(page = page, per_page = per_page)

	return render_template('home.html', title = 'Home page', items = items)