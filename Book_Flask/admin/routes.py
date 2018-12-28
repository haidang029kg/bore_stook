from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from Book_Flask import db, bcrypt
from Book_Flask.models import User, OrderDetails, Orders, Ispaid, Status, Paymentmethod, Book, Author, admin_login_required
from Book_Flask.admin.forms import AddBookForm, AdminLoginForm
from flask_login import login_user, logout_user, current_user, login_required


admin = Blueprint('admin', __name__)


@admin.route("/admin_dashboard/chart")
@admin_login_required  # be defined in model
def dashboard():
    try:
        yesterdaySales = int(db.session.execute(
            'select sum(TotalPrice) from orders where DATE(Date)=DATE(SUBDATE(NOW(),1));').fetchall()[0][0])
        print(yesterdaySales)
    except:
        yesterdaySales = 0

    try:
        yesterdayOrders = int(db.session.execute(
            'select count(*) from orders where DATE(Date)=DATE(SUBDATE(NOW(),1));').fetchall()[0][0])
    except:
        yesterdayOrders = 0

    try:
        yesterdayBooks = int(db.session.execute(
            'select sum(Quantity) from (select OrderID from orders where DATE(Date)=DATE(SUBDATE(NOW(),1))) as OrderIDList, order_details where OrderIDList.OrderID = order_details.OrderID;').fetchall()[0][0])
    except:
        yesterdayBooks = 0

    try:
        todaySales = int(db.session.execute(
            'select sum(TotalPrice) from orders where DATE(Date)=DATE(NOW());').fetchall()[0][0])
    except:
        todaySales = 0

    try:
        todayOrders = int(db.session.execute(
            'select count(*) from orders where DATE(Date)=DATE(NOW());').fetchall()[0][0])
    except:
        todayOrders = 0

    try:
        todayBooks = int(db.session.execute(
            'select sum(Quantity) from (select OrderID from orders where DATE(Date)=DATE(NOW())) as OrderIDList, order_details where OrderIDList.OrderID = order_details.OrderID;').fetchall()[0][0])
    except:
        todayBooks = 0

    return render_template('admin/chart.html', yesterdaySales=yesterdaySales, yesterdayOrders=yesterdayOrders, yesterdayBooks=yesterdayBooks,
                           todaySales=todaySales, todayOrders=todayOrders, todayBooks=todayBooks)


@admin.route("/admin_dashboard/order_management")
@admin_login_required
def order_management():

    page = request.args.get('page', 1, type=int)
    per_page = 10

    items = db.session.query(Orders.OrderID, Orders.Date, User.Email, User.FirstName, User.LastName, Orders.Address, Orders.Phone, Orders.TotalPrice, Ispaid.NamePaid,
                             Paymentmethod.NamePayment, Status.NameStatus).join(Ispaid).join(Status).join(Paymentmethod).join(User).order_by(Orders.Date.desc()).paginate(page=page, per_page=per_page)

    return render_template('admin/order_management.html', items=items, task_name='management')


@admin.route("/admin_ordered_search", methods=['POST', 'GET'])
@admin_login_required
def ordered_searching():
    value_search = request.form.get('input-search-ordered')

    if not value_search:
        value_search = request.args.get('value_search')

    page = request.args.get('page', 1, type=int)
    per_page = 5

    if value_search:
        # search by ordered id firstly
        items = db.session.query(Orders.OrderID).filter(Orders.OrderID.contains(value_search)).join(
            Ispaid).join(Status).join(Paymentmethod).join(User).first()
        user_id = ''
        if items is None:
            # search by customer's email secondly
            user = db.session.query(User.UserID).filter(
                User.Email.contains(value_search)).first()

            if user is None:
                # not found at all
                items = []
                return render_template('admin/order_management_without_pages.html', items=items)
            else:
                user_id = user[0]
                items = db.session.query(Orders.OrderID, Orders.Date, User.Email, User.FirstName, User.LastName, Orders.Address, Orders.Phone, Orders.TotalPrice, Ispaid.NamePaid, Paymentmethod.NamePayment, Status.NameStatus).filter(
                    Orders.UserID == user_id).join(Ispaid).join(Status).join(Paymentmethod).join(User).order_by(Orders.Date.desc()).paginate(page=page, per_page=per_page)
                return render_template('admin/order_management.html', items=items, value_search=value_search)
        else:
            items = db.session.query(Orders.OrderID, Orders.Date, User.Email, User.FirstName, User.LastName, Orders.Address, Orders.Phone, Orders.TotalPrice, Ispaid.NamePaid, Paymentmethod.NamePayment,
                                     Status.NameStatus).filter(Orders.OrderID.contains(value_search)).join(Ispaid).join(Status).join(Paymentmethod).join(User).paginate(page=page, per_page=per_page)
            return render_template('admin/order_management.html', items=items, value_search=value_search)

    else:
        value_search = request.args.get('value_search')

        if value_search:
            user_id = db.session.query(User.UserID).filter(
                User.Email == value_search).first()[0]
            items = db.session.query(Orders.OrderID, Orders.Date, User.Email, User.FirstName, User.LastName, Orders.Address, Orders.Phone, Orders.TotalPrice, Ispaid.NamePaid, Paymentmethod.NamePayment, Status.NameStatus).filter(
                Orders.UserID == user_id).join(Ispaid).join(Status).join(Paymentmethod).join(User).order_by(Orders.Date.desc()).paginate(page=page, per_page=per_page)

            return render_template('admin/order_management.html', items=items, value_search=value_search)

    return redirect(url_for('admin.order_management'))


@admin.route("/admin_ordered_detail", methods=['GET'])
@admin_login_required
def ordered_detail():
    ordered_id = request.args.get('ordered_id')

    items = db.session.query(Book.ImgUrl, Book.Title, Book.Price, OrderDetails.Quantity).filter(
        OrderDetails.OrderID == ordered_id).filter(OrderDetails.OrderID == Orders.OrderID).filter(OrderDetails.BookID == Book.BookID).all()
    total_price = db.session.query(Orders.TotalPrice).filter(
        Orders.OrderID == ordered_id).first()[0]

    return jsonify({
        'ordered_id': ordered_id,
        'total_price': total_price,
        'items': items
    })


@admin.route("/admin_change_order_status", methods=['GET'])
@admin_login_required
def change_order_status():
    status_id = request.args.get('radio_value_status')
    paid_id = request.args.get('radio_value_paid')
    order_id = request.args.get('order_id')

    if (order_id) and (status_id) and(paid_id):

        db.session.query(Orders).filter(Orders.OrderID == order_id).update(
            {Orders.Status: status_id, Orders.IsPaid: paid_id})
        db.session.commit()

        flash("Changing Order's Status Is Done", 'info')

        return jsonify({'status': 'done'})
    return jsonify({'status': 'error'})


@admin.route("/top_genre")
@admin_login_required
def top_genre():
    items = db.session.execute('select Name, order_count from (select GenreID, sum(order_details.Quantity) as order_count from order_details, book where book.BookID = order_details.BookID group by GenreID) as genre_count, genre where genre_count.GenreID = genre.GenreID order by order_count desc limit 5;')
    di = dict()
    for k, v in items.fetchall():
        di[k] = v

    return jsonify(di)


@admin.route("/sales5days")
@admin_login_required
def sales5days():
    items = db.session.execute(
        'select DATE(Date), sum(TotalPrice) from orders group by DATE(Date) order by DATE(Date) desc limit 5;')
    di = dict()
    for k, v in items.fetchall():
        di[str(k)] = v

    return jsonify(di)


@admin.route("/admin_dashboard/book_management", methods=['GET', 'POST'])
@admin_login_required
def book_management():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    items = db.session.query(Book.BookID, Book.ImgUrl, Book.Title, Book.ISBN, Book.Price).order_by(
        Book.BookID.desc()).paginate(page=page, per_page=per_page)

    return render_template('admin/book_management.html', items=items)


@admin.route("/admin_dashboard/book_searching", methods=['GET', 'POST'])
@admin_login_required
def book_searching():
    value_search = request.form.get('input-search-book')
    page = request.args.get('page', 1, type=int)
    per_page = 5

    if not value_search:
        value_search = request.args.get('value_search')

    if value_search:
        items = db.session.query(Book.BookID, Book.ImgUrl, Book.Title, Book.ISBN, Book.Price).filter(
            Book.ISBN.contains(value_search)).first()

        if items is None:
            items = db.session.query(Book.BookID, Book.ImgUrl, Book.Title, Book.ISBN, Book.Price).filter(
                Book.Title.contains(value_search)).first()

            if items is None:
                items = []

                return render_template('admin/book_management_without_pages.html', items=items, value_search = value_search)

            else:
                items = db.session.query(Book.BookID, Book.ImgUrl, Book.Title, Book.ISBN, Book.Price).filter(
                    Book.Title.contains(value_search)).order_by(Book.BookID.desc()).paginate(page=page, per_page=per_page)
                return render_template('admin/book_management.html', items=items, value_search=value_search)
        else:
            items = db.session.query(Book.BookID, Book.ImgUrl, Book.Title, Book.ISBN, Book.Price).filter(
                Book.ISBN.contains(value_search)).order_by(Book.BookID.desc()).paginate(page=page, per_page=per_page)

            return render_template('admin/book_management.html', items=items, value_search=value_search)
    else:
        flash('input search is empty!!!', 'info')
        return redirect(url_for('admin.book_management'))

@admin.route("/admin_dashboard/delete_book", methods = ['GET'])
@admin_login_required
def delete_book():
    book_id = request.args.get('book_id')

    book = Book.query.filter_by(BookID = book_id).first()

    if book:
        db.session.delete(book)
        db.session.commit()
        
        flash('book is deleted', 'info')

        return jsonify({'status':'done'})
    return jsonify({'status':'error'})

@admin.route("/admin_dashboard/user_management", methods=['GET'])
@admin_login_required
def user_management():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    items = db.session.query(User.UserID, User.Email, User.FirstName,
                             User.LastName, User.Phone).filter(User.RoleAdmin == False).paginate(page=page, per_page=per_page)

    count = db.session.query(User.UserID).count()

    return render_template('admin/user_management.html', items=items, count=count)


@admin.route("/admin_dashboard_user_searching", methods=['GET', 'POST'])
@admin_login_required
def user_searching():
    value_search = request.form.get('input-search-user')
    page = request.args.get('page', 1, type=int)
    per_page = 5

    if not value_search:
        value_search = request.args.get('value_search')

    if value_search:
        items = db.session.query(User.UserID).filter(User.RoleAdmin == False).filter(
            User.Email.contains(value_search)).first()
        if items is None:
            items = []

            return render_template('admin/user_management_without_pages.html', items=items, value_search=value_search)
        else:
            items = db.session.query(User.UserID, User.Email, User.FirstName, User.LastName, User.Phone).filter(User.RoleAdmin == False).filter(
                User.Email.contains(value_search)).paginate(page=page, per_page=per_page)

            return render_template('admin/user_management.html', items=items, value_search=value_search)

    # input search is empty
    return redirect(url_for('admin.user_management'))


@admin.route("/admin_dashboard_reset_user", methods=['GET'])
@admin_login_required
def admin_dashboard_reset_pass():
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)

    if user:
        hashed_password = bcrypt.generate_password_hash('123').decode('utf-8')

        user.Password = hashed_password

        db.session.commit()

        return jsonify({'status': 'done'})
    return jsonify({'status': 'error'})


@admin.route("/admin_dashboard/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin.dashboard'))

    logout_user()
    form = AdminLoginForm()

    if form.validate_on_submit():

        admin = User.query.filter_by(Email=form.email.data).first()

        if admin and bcrypt.check_password_hash(admin.Password, form.password.data):
            login_user(admin, remember=True)

            next_page = request.args.get('next')
            flash('Login successful!', 'success')

            return redirect(next_page) if next_page else redirect(url_for('admin.dashboard'))

    return render_template('admin/login.html', form=form)


@admin.route("/admin_dashboard/addbook", methods=['GET', 'POST'])
@admin_login_required
def addbook():

    form = AddBookForm()

    if form.validate_on_submit():
        authorList = ''
        for author in form.author.data:
            authorID = db.session.query(Author.AuthorID).filter(
                Author.Name == author).all()

            if authorID:
                authorList = authorList + str(authorID[0][0]) + ','
            else:
                # Add new author
                author = Author(Name=author)
                db.session.add(author)
                db.session.commit()
                authorList = authorList + str(author.getAuthorID()) + ','
        print(authorList[:-1])
        book = Book(Title=form.title.data,
                    ISBN=form.ISBN.data,
                    AuthorsID=authorList[:-1],
                    PublicationYear=form.publicationYear.data,
                    ImgUrl=form.imgUrl.data,
                    Price=form.price.data,
                    AvgRating=form.avgRating.data,
                    Quantity=form.quantity.data,
                    GenreID=form.genre.data)
        db.session.add(book)
        db.session.commit()
        flash('Book is added!!!', 'info')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/addbook.html', form=form)
