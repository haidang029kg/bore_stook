from flask import render_template, request, Blueprint, jsonify, json
from Book_Flask.models import Book
from Book_Flask import db

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
	page = request.args.get('page', 1, type = int)
	per_page = 20

	#items = Book.query.order_by(Book.Title.asc()).paginate(page = page, per_page = per_page)
	items = db.session.query(Book.BookID, Book.Title, Book.ImgUrl, Book.Price).order_by(Book.Title.asc()).paginate(page = page, per_page = per_page)
	db.session.close()
	
	return render_template('home.html', title = 'Home page', items = items)




@main.route("/book_detail", methods = ['POST'])
def book_detail():
	book_id = request.form.getlist('id') # if using POST method
	#book_id = request.args.getlist('id') # if using GET method
	book_id = int(book_id[0])
	
	book_temp = Book.query.get(book_id)

	string_temp = 'select Name from genre where GenreID = ' + str(book_temp.GenreID)
	genre_name = db.session.execute(string_temp).first()[0]
	
	#list_authorID = book_temp.AuthorsID.split(',')
	
	#list_authorName = []

	#for i in list_authorID:
	#	string_temp = 'select Name from author where AuthorID = ' + str(i)
	#	list_authorName.append(str(db.session.execute(string_temp).first()[0]))
	
	#dic_author = dict(zip(list_authorID, list_authorName))
	db.session.close()

	if book_temp:
		return jsonify({'BookID' : book_temp.BookID,
						'Title' : book_temp.Title,
						'ISBN' : book_temp.ISBN,
						'Price' : book_temp.Price,
						'ImgUrl' : book_temp.ImgUrl,
						'Quantity' : book_temp.Quantity,
						'AvgRating' : book_temp.AvgRating,
						'PublicationYear' : book_temp.PublicationYear,
						'AuthorsID' : book_temp.AuthorsID,
						'GenreID' : book_temp.GenreID,
						'GenreName' : genre_name})
	
	return jsonify({'error' : 'Wrong!'})