from flask import render_template, request, Blueprint, jsonify, json, flash
from Book_Flask.models import Book, Author, Genre, Orders, OrderDetails, generate_id
from Book_Flask import db
from flask_login import login_required

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    per_page = 20

    items = db.session.query(Book.BookID, Book.Title, Book.ImgUrl, Book.Price).order_by(
        Book.Title.asc()).paginate(page=page, per_page=per_page)

    genre_items = db.session.query(Genre.GenreID, Genre.Name).order_by(Genre.Name).all()
    newly_items = db.session.query(Book.BookID, Book.Title, Book.ImgUrl, Book.Price).order_by(Book.BookID.desc()).limit(10).all()

    db.session.close()

    return render_template('home.html', title='Home page', items=items, genre_items = genre_items, newly_items = newly_items)


@main.route("/home/author/<int:authorid>", methods=['GET'])
def home_author(authorid):
    string_temp = 'select BookID, Title, ImgUrl, Price from book where FIND_IN_SET(+' + str(
        authorid) + ', AuthorsID);'

    items = db.session.execute(string_temp).fetchall()

    author_name = db.session.query(Author.Name).filter_by(
        AuthorID=authorid).first()[0]
    count_result = len(items)

    genre_items = db.session.query(Genre.GenreID, Genre.Name).order_by(Genre.Name).all()
    newly_items = db.session.query(Book.BookID, Book.Title, Book.ImgUrl, Book.Price).order_by(Book.BookID.desc()).limit(10).all()

    db.session.close()

    flash(str(count_result) + ' results for ' + author_name, 'info')

    return render_template('home.html', title='Filter by author', items=items, genre_items = genre_items, newly_items = newly_items, task_name = 'Search Result For Author: ' + author_name)


@main.route("/home/genre/<int:genreid>", methods=['GET'])
def home_genre(genreid):
    page = request.args.get('page', 1, type=int)
    per_page = 20

    items = db.session.query(Book.BookID, Book.Title, Book.ImgUrl, Book.Price).filter_by(
        GenreID=genreid).order_by(Book.Title.asc()).paginate(page=page, per_page=per_page)

    genre_name = db.session.query(Genre.Name).filter_by(
        GenreID=genreid).first()[0]
    count_result = db.session.query(
        Book.BookID).filter_by(GenreID=genreid).count()


    genre_items = db.session.query(Genre.GenreID, Genre.Name).order_by(Genre.Name).all()
    newly_items = db.session.query(Book.BookID, Book.Title, Book.ImgUrl, Book.Price).order_by(Book.BookID.desc()).limit(10).all()

    db.session.close()

    flash(str(count_result) + ' results for ' + genre_name, 'info')

    return render_template('home.html', title='Filter by genre', items=items, genreid=genreid, genre_items = genre_items, newly_items = newly_items, task_name = 'Search Result For Genre: ' + genre_name)


@main.route("/book_detail", methods=['POST'])
def book_detail():
    book_id = request.form.getlist('id')  # if using POST method
    # book_id = request.args.getlist('id') # if using GET method
    book_id = int(book_id[0])

    book_temp = Book.query.get(book_id)

    string_temp = 'select Name from genre where GenreID = ' + \
        str(book_temp.GenreID)
    genre_name = db.session.execute(string_temp).first()[0]

    db.session.close()

    if book_temp:
        return jsonify({'BookID': book_temp.BookID,
                        'Title': book_temp.Title,
                        'ISBN': book_temp.ISBN,
                        'Price': book_temp.Price,
                        'ImgUrl': book_temp.ImgUrl,
                        'Quantity': book_temp.Quantity,
                        'AvgRating': book_temp.AvgRating,
                        'PublicationYear': book_temp.PublicationYear,
                        'AuthorsID': book_temp.AuthorsID,
                        'GenreID': book_temp.GenreID,
                        'GenreName': genre_name})

    return jsonify({'error': 'error!'})


@main.route("/list_authors", methods=['POST'])
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

    return jsonify({'error': 'error!'})


@main.route("/cart")
def cart():
    return render_template('cart.html')


@main.route("/checkout")
@login_required
def checkout():
    return render_template('checkout.html')


@main.route("/home/searching", methods=['GET', 'POST'])
def searching():
    value_search = request.form.get('input-search')
    value_search_adv = request.form.get('input-search-adv')
    type_search_adv = request.form.get('input-type-search-adv')

    counters = None
    items = None
    page = request.args.get('page', 1, type=int)
    per_page = 20
    genreid = 0

    if (value_search_adv): # advance search
        if (int(type_search_adv) == 0):# search by Title
            items = db.session.query(Book.BookID).filter(Book.Title.contains(value_search_adv)).first()
            if (items is None):
                items = []
                counters = 0
            else:
                items = db.session.query(Book.BookID, Book.Title, Book.ImgUrl, Book.Price).filter(Book.Title.contains(value_search_adv)).order_by(Book.Title.asc()).paginate(page=page, per_page=per_page)
                counters = db.session.query(Book.BookID).filter(Book.Title.contains(value_search_adv)).count()
            task_name = 'Title: ' + value_search_adv
        if (int(type_search_adv) == 1):# search by ISBN
            items = db.session.query(Book.BookID).filter(Book.ISBN == value_search_adv).first()
            if (items is None):
                items = []
                counters = 0
            else:
                items = db.session.query(Book.BookID, Book.Title, Book.ImgUrl, Book.Price).filter(Book.ISBN == value_search_adv)
                counters = 1
            task_name = 'ISBN: ' + str(value_search_adv)
        if (int(type_search_adv) == 2):# search by Author
            author = db.session.query(Author.AuthorID, Author.Name).filter(Author.Name.contains(value_search_adv)).first()
            if (author is None):
                items = []
                counters = 0
            else:
                authorid = author[0]
                string_sql = 'select BookID, Title, ImgUrl, Price from book where FIND_IN_SET(+' + str(authorid) + ', AuthorsID);'

                items = db.session.execute(string_sql).fetchall()
                counters = len(items)
            task_name = 'Author: ' + value_search_adv

        if (int(type_search_adv) == 3):# search by Genre
            genre = db.session.query(Genre.GenreID, Genre.Name).filter(Genre.Name.contains(value_search_adv)).first()
            if (genre is None):
                items = []
                counters = 0
            else:
                genreid = genre[0]

                items = db.session.query(Book.BookID, Book.Title, Book.ImgUrl, Book.Price).filter(Book.GenreID == genreid).order_by(Book.Title.asc()).paginate(page = page, per_page = per_page)
                counters = db.session.query(Book.BookID, Book.Title, Book.ImgUrl, Book.Price).filter(Book.GenreID == genreid).count()
            task_name = 'Genre: ' + value_search_adv
        
        genre_items = db.session.query(Genre.GenreID, Genre.Name).order_by(Genre.Name).all()
        newly_items = db.session.query(Book.BookID, Book.Title, Book.ImgUrl, Book.Price).order_by(Book.BookID.desc()).limit(10).all()
        
        db.session.close()
        flash(str(counters) + ' results for ' + value_search_adv, 'info')
        return render_template('home.html', items=items, value_search=value_search_adv, genreid = genreid, title='Searching', genre_items = genre_items, newly_items = newly_items, task_name = 'Search Result For ' + task_name)
        
    elif (value_search):# search from input in main navagation bar and search by Title
        items = db.session.query(Book.BookID).filter(Book.Title.contains(value_search)).first()
        if (items is None):
            items = []
            counters = 0
        else:
            items = db.session.query(Book.BookID, Book.Title, Book.ImgUrl, Book.Price).filter(Book.Title.contains(value_search)).order_by(Book.Title.asc()).paginate(page=page, per_page=per_page)
            counters = db.session.query(Book.BookID).filter(Book.Title.contains(value_search)).count()

        genre_items = db.session.query(Genre.GenreID, Genre.Name).order_by(Genre.Name).all()
        newly_items = db.session.query(Book.BookID, Book.Title, Book.ImgUrl, Book.Price).order_by(Book.BookID.desc()).limit(10).all()

        flash(str(counters) + ' results for ' + value_search, 'info')
        return render_template('home.html', items=items, value_search=value_search, title='Searching', genre_items = genre_items, newly_items = newly_items, task_name = 'Search Result For Title: ' + value_search)
        
    else: # switching in pages
        value_search = request.args.get('value_search')

        items = db.session.query(Book.BookID, Book.Title, Book.ImgUrl, Book.Price).filter(Book.Title.contains(value_search)).order_by(Book.Title.asc()).paginate(page=page, per_page=per_page)
        
        genre_items = db.session.query(Genre.GenreID, Genre.Name).order_by(Genre.Name).all()
        newly_items = db.session.query(Book.BookID, Book.Title, Book.ImgUrl, Book.Price).order_by(Book.BookID.desc()).limit(10).all()

        return render_template('home.html', items=items, value_search=value_search_adv, title='Searching', genre_items = genre_items, newly_items = newly_items, task_name = 'Search Result For: ' + value_search)
    
    return render_template('home.html', items=items, title='Searching')