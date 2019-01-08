from flask import render_template, request, Blueprint, jsonify, json, flash, redirect, url_for
from Book_Flask.models import Book, Author, Genre, Orders, OrderDetails, generate_id, Rules
from Book_Flask import db
from flask_login import login_required
from Book_Flask.main.utilities import *

main = Blueprint('main', __name__)


@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    per_page = 20

    items = db.session.query(Book.BookID, Book.Title, Book.ImgUrl, Book.Price).order_by(
        Book.Title.asc()).paginate(page=page, per_page=per_page)

    genre_items = db.session.query(
        Genre.GenreID, Genre.Name).order_by(Genre.Name).all()
    newly_items = db.session.query(Book.BookID, Book.Title, Book.ImgUrl, Book.Price).order_by(
        Book.BookID.desc()).limit(10).all()

    return render_template('home.html', title='Home page', items=items, genre_items=genre_items, newly_items=newly_items)


@main.route("/home/author/<int:authorid>", methods=['GET'])
def home_author(authorid):
    string_temp = 'select BookID, Title, ImgUrl, Price from book where FIND_IN_SET(+' + str(
        authorid) + ', AuthorsID);'

    items = db.session.execute(string_temp).fetchall()

    author_name = db.session.query(Author.Name).filter_by(
        AuthorID=authorid).first()[0]
    count_result = len(items)

    genre_items = db.session.query(
        Genre.GenreID, Genre.Name).order_by(Genre.Name).all()
    newly_items = db.session.query(Book.BookID, Book.Title, Book.ImgUrl, Book.Price).order_by(
        Book.BookID.desc()).limit(10).all()

    flash(str(count_result) + ' results for ' + author_name, 'info')

    return render_template('home.html', title='Filter by author', items=items, genre_items=genre_items, newly_items=newly_items, task_name='Search Result For Author: ' + author_name)


@main.route("/home/genre/<int:genreid>", methods=['GET'])
def home_genre(genreid):
    page = request.args.get('page', 1, type=int)
    per_page = 20

    genre_name = db.session.query(Genre.Name).filter_by(
        GenreID=genreid).first()[0]
    count_result = db.session.query(
        Book.BookID).filter_by(GenreID=genreid).count()

    if count_result == 0:
        items = []
    else:
        items = db.session.query(Book.BookID, Book.Title, Book.ImgUrl, Book.Price).filter_by(
            GenreID=genreid).order_by(Book.Title.asc()).paginate(page=page, per_page=per_page)

    genre_items = db.session.query(
        Genre.GenreID, Genre.Name).order_by(Genre.Name).all()
    newly_items = db.session.query(Book.BookID, Book.Title, Book.ImgUrl, Book.Price).order_by(
        Book.BookID.desc()).limit(10).all()

    flash(str(count_result) + ' results for ' + genre_name, 'info')

    if items is None:
        items = []

    return render_template('home.html', title='Filter by genre', items=items, genreid=genreid, genre_items=genre_items, newly_items=newly_items, task_name='Search Result For Genre: ' + genre_name)


@main.route("/book_detail", methods=['POST'])
def book_detail():
    book_id = request.form.getlist('id')  # if using POST method
    # book_id = request.args.getlist('id') # if using GET method
    book_id = int(book_id[0])

    book_temp = Book.query.get(book_id)

    string_temp = 'select Name from genre where GenreID = ' + \
        str(book_temp.GenreID)
    genre_name = db.session.execute(string_temp).first()[0]

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


@main.route("/related_book_by_genre", methods=['GET'])
def random_book_by_genre():

    genre_id = request.args.get('genre_id')

    if genre_id:
        string_sql = 'select BookID, Title, ImgUrl, Price from book where GenreID = ' + \
            str(genre_id) + ' ORDER BY RAND() limit 6;'

        items = db.session.execute(string_sql).fetchall()

        items = json.dumps([dict(i) for i in items])
        return jsonify({
            'items': items
        })
    return jsonify({
        'error': 'error'
    })


@main.route("/books_also_be_bought", methods=['GET'])
def books_also_be_bouth():

    book_id = request.args.get('book_id')

    items = db.session.query(Rules.Consequents).filter(
        Rules.Antecendents == book_id).all()

    books_id_also_be_bought = []

    for i in items:
        books_id_also_be_bought.append(i[0])

    items_id = []
    for i in books_id_also_be_bought:
        if ',' in i:
            for i2 in i.split(','):
                if i2 not in items_id:
                    items_id.append(i2)
        else:
            if i not in items_id:
                items_id.append(i)

    if len(items_id) > 6:
        items_id = items_id[:6]

    items = []
    for i in items_id:
        item = db.session.query(Book.BookID, Book.Title, Book.ImgUrl, Book.Price).filter(
            Book.BookID == i).first()
        items.append(item)

    if len(items) > 0:
        items = json.dumps(items)
        return jsonify({'items': items})

    else:
        return jsonify({'status': 'not_available'})


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

    dict_authors = dict(zip(lis_ids, lis_names))

    if dict_authors:
        return jsonify(dict_authors)

    return jsonify({'error': 'error!'})


@main.route("/cart")
def cart():
    return render_template('cart.html')


@main.route("/loading_recommendation", methods=['POST'])
def loading_recommendation():
    cart = request.form.get('cart_data')
    cart = json.loads(cart)

    book_ids_cart = []
    [book_ids_cart.append(x['bookid']) for x in cart]

    book_ids_rule = []
    items_rule = db.session.query(Rules.Antecendents).all()

    for i in items_rule:
        ids = i[0].split(',')
        ids = set(ids)
        book_ids_rule.append(ids)

    book_ids_cart_combination = making_combination(book_ids_cart)

    result = making_recommendation(book_ids_cart_combination, book_ids_rule)

    if len(result) > 0:

        book_ids_for_recommendation = []
        book_ids_for_recommendation_less_priority = []
        for i in result:
            temp = db.session.query(Rules.Consequents).filter(
                Rules.Antecendents == i).first()
            if temp:
                if ',' in temp[0]:
                    [book_ids_for_recommendation.append(x) for x in temp[0].split(
                        ',') if x not in book_ids_for_recommendation]
                elif temp[0] not in book_ids_for_recommendation:
                    book_ids_for_recommendation.append(temp[0])

            if ',' not in i:
                string_sql = 'select Consequents from rules where FIND_IN_SET(' + str(i) + ', Antecendents);'
                items = db.session.execute(string_sql).fetchall()

                for i2 in items:
                    [book_ids_for_recommendation_less_priority.append(x) for x in i2[0].split(',') if x not in book_ids_for_recommendation_less_priority]



        [book_ids_for_recommendation.append(
            x) for x in book_ids_for_recommendation_less_priority if x not in book_ids_for_recommendation]

        final_result_items = []
        for i in book_ids_for_recommendation:
            item = db.session.query(Book.BookID, Book.Title, Book.ImgUrl, Book.Price).filter(
                Book.BookID == i).first()
            if item:
                final_result_items.append(item)

        final_result_items = json.dumps(final_result_items)
        return jsonify({'items': final_result_items})

    else:
        return jsonify({'status': 'not_available'})


@main.route("/checkout")
@login_required
def checkout():
    return render_template('checkout.html')


@main.route("/home/searching", methods=['GET', 'POST'])
def searching():
    value_search = request.form.get('input-search')
    value_search_adv = request.form.get('input-search-adv')
    type_search_adv = request.form.get('input-type-search-adv')

    if (not value_search_adv) and (not value_search):  # input is none
        return redirect(url_for('main.home'))

    counters = None
    items = None
    page = request.args.get('page', 1, type=int)
    per_page = 20
    genreid = 0

    if (value_search_adv):  # advance search
        if (int(type_search_adv) == 0):  # search by Title
            items = db.session.query(Book.BookID).filter(
                Book.Title.contains(value_search_adv)).first()
            if (items is None):
                items = []
                counters = 0
            else:
                items = db.session.query(Book.BookID, Book.Title, Book.ImgUrl, Book.Price).filter(
                    Book.Title.contains(value_search_adv)).order_by(Book.Title.asc()).paginate(page=page, per_page=per_page)
                counters = db.session.query(Book.BookID).filter(
                    Book.Title.contains(value_search_adv)).count()
            task_name = 'Title: ' + value_search_adv
        if (int(type_search_adv) == 1):  # search by ISBN
            items = db.session.query(Book.BookID).filter(
                Book.ISBN == value_search_adv).first()
            if (items is None):
                items = []
                counters = 0
            else:
                items = db.session.query(Book.BookID, Book.Title, Book.ImgUrl, Book.Price).filter(
                    Book.ISBN == value_search_adv)
                counters = 1
            task_name = 'ISBN: ' + str(value_search_adv)
        if (int(type_search_adv) == 2):  # search by Author
            author = db.session.query(Author.AuthorID, Author.Name).filter(
                Author.Name.contains(value_search_adv)).first()
            if (author is None):
                items = []
                counters = 0
            else:
                authorid = author[0]
                string_sql = 'select BookID, Title, ImgUrl, Price from book where FIND_IN_SET(+' + str(
                    authorid) + ', AuthorsID);'

                items = db.session.execute(string_sql).fetchall()
                counters = len(items)
            task_name = 'Author: ' + value_search_adv

        if (int(type_search_adv) == 3):  # search by Genre
            genre = db.session.query(Genre.GenreID, Genre.Name).filter(
                Genre.Name.contains(value_search_adv)).first()
            if (genre is None):
                items = []
                counters = 0
            else:
                genreid = genre[0]

                items = db.session.query(Book.BookID, Book.Title, Book.ImgUrl, Book.Price).filter(
                    Book.GenreID == genreid).order_by(Book.Title.asc()).paginate(page=page, per_page=per_page)
                counters = db.session.query(Book.BookID, Book.Title, Book.ImgUrl, Book.Price).filter(
                    Book.GenreID == genreid).count()
            task_name = 'Genre: ' + value_search_adv

        genre_items = db.session.query(
            Genre.GenreID, Genre.Name).order_by(Genre.Name).all()
        newly_items = db.session.query(Book.BookID, Book.Title, Book.ImgUrl, Book.Price).order_by(
            Book.BookID.desc()).limit(10).all()

        flash(str(counters) + ' results for ' + value_search_adv, 'info')
        return render_template('home.html', items=items, value_search=value_search_adv, genreid=genreid, title='Searching', genre_items=genre_items, newly_items=newly_items, task_name='Search Result For ' + task_name)

    elif not value_search:  # input is none
        return redirect(url_for('main.home'))

    elif (value_search):  # search from input in main navagation bar and search by Title
        items = db.session.query(Book.BookID).filter(
            Book.Title.contains(value_search)).first()
        if (items is None):
            items = []
            counters = 0
        else:
            items = db.session.query(Book.BookID, Book.Title, Book.ImgUrl, Book.Price).filter(
                Book.Title.contains(value_search)).order_by(Book.Title.asc()).paginate(page=page, per_page=per_page)
            counters = db.session.query(Book.BookID).filter(
                Book.Title.contains(value_search)).count()

        genre_items = db.session.query(
            Genre.GenreID, Genre.Name).order_by(Genre.Name).all()
        newly_items = db.session.query(Book.BookID, Book.Title, Book.ImgUrl, Book.Price).order_by(
            Book.BookID.desc()).limit(10).all()

        flash(str(counters) + ' results for ' + value_search, 'info')
        return render_template('home.html', items=items, value_search=value_search, title='Searching', genre_items=genre_items, newly_items=newly_items, task_name='Search Result For Title: ' + value_search)

    else:  # switching in pages
        value_search = request.args.get('value_search')

        items = db.session.query(Book.BookID, Book.Title, Book.ImgUrl, Book.Price).filter(
            Book.Title.contains(value_search)).order_by(Book.Title.asc()).paginate(page=page, per_page=per_page)

        genre_items = db.session.query(
            Genre.GenreID, Genre.Name).order_by(Genre.Name).all()
        newly_items = db.session.query(Book.BookID, Book.Title, Book.ImgUrl, Book.Price).order_by(
            Book.BookID.desc()).limit(10).all()

        return render_template('home.html', items=items, value_search=value_search_adv, title='Searching', genre_items=genre_items, newly_items=newly_items, task_name='Search Result For: ' + value_search)

    return render_template('home.html', items=items, title='Searching')
