from flask import render_template, request, Blueprint, jsonify, json
from Book_Flask.models import Book
from Book_Flask import db

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
	page = request.args.get('page', 1, type = int)
	per_page = 20

	items = db.session.query(Book.BookID, Book.Title, Book.ImgUrl, Book.Price).order_by(Book.Title.asc()).paginate(page = page, per_page = per_page)
	db.session.close()

	return render_template('home.html', title = 'Home page', items = items)



@main.route("/home/author/<int:authorid>", methods = ['GET'])
def home_author(authorid):
	string_temp = 'select BookID, Title, ImgUrl, Price from book where FIND_IN_SET(+' + str(authorid) + ', AuthorsID);'
	
	items = db.session.execute(string_temp).fetchall()

	db.session.close()

	return render_template('home.html', title = 'Filter by author', items = items)



@main.route("/home/genre/<int:genreid>", methods = ['GET'])
def home_genre(genreid):
	page = request.args.get('page', 1, type = int)
	per_page = 20

	items = db.session.query(Book.BookID, Book.Title, Book.ImgUrl, Book.Price).filter_by(GenreID = genreid).order_by(Book.Title.asc()).paginate(page = page, per_page = per_page)
	
	db.session.close()

	return render_template('home.html', title = 'Filter by gnere', items = items)

@main.route("/book_detail", methods = ['POST'])
def book_detail():
	book_id = request.form.getlist('id') # if using POST method
	#book_id = request.args.getlist('id') # if using GET method
	book_id = int(book_id[0])
	
	book_temp = Book.query.get(book_id)

	string_temp = 'select Name from genre where GenreID = ' + str(book_temp.GenreID)
	genre_name = db.session.execute(string_temp).first()[0]
	
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
	
	return jsonify({'error' : 'error!'})


@main.route("/list_authors", methods = ['POST'])
def list_authors():
	string_ids = request.form.getlist('list_id')
	string_ids = string_ids[0]

	lis_ids = string_ids.split(',')
	lis_names = []

	for i in lis_ids:
		i = i.strip()
		string_temp = 'select Name from author where AuthorID = ' + str(i)
		lis_names.append(db.session.execute(string_temp).first()[0])

	db.session.close()

	dict_authors = dict(zip(lis_ids, lis_names))
	
	if dict_authors:
		return jsonify(dict_authors)

	return jsonify({'error' : 'error!'})