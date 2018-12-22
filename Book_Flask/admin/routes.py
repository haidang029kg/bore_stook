
from flask import Blueprint, render_template, request, jsonify
from Book_Flask import db
from Book_Flask.models import User, OrderDetails, Orders , Ispaid, Status, Paymentmethod, Book
from Book_Flask.user.forms import AddBookForm


admin = Blueprint('admin', __name__)


@admin.route("/admin_dashboard/chart")
def dashboard():
    return  render_template('admin/chart.html')

@admin.route("/admin_dashboard/order_management")
def order_management():

    page = request.args.get('page',1 , type=int)
    per_page = 10

    items = db.session.query(Orders.OrderID, Orders.Date, Orders.UserID, User.FirstName, User.LastName, Orders.Address, Orders.Phone, Orders.TotalPrice, Ispaid.NamePaid, Paymentmethod.NamePayment, Status.NameStatus).join(Ispaid).join(Status).join(Paymentmethod).join(User).order_by(Orders.Date.desc()).paginate(page = page, per_page = per_page)
    
    return render_template('admin/order_management.html', items = items)


@admin.route("/admin_ordered_detail", methods = ['GET'])
def ordered_detail():
    ordered_id = request.args.get('ordered_id')

    items = db.session.query(Book.ImgUrl, Book.Title, Book.Price, OrderDetails.Quantity).filter(OrderDetails.OrderID == ordered_id).filter(OrderDetails.OrderID == Orders.OrderID).filter(OrderDetails.BookID == Book.BookID).all()
    total_price = db.session.query(Orders.TotalPrice).filter(Orders.OrderID == ordered_id).first()[0]


    return jsonify({
        'ordered_id' : ordered_id,
        'total_price' : total_price,
        'items' : items
    })

@admin.route("/admin_change_order_status", methods = ['GET'])
def change_order_status():
    status_id = request.args.get('radio_value_status')
    paid_id = request.args.get('radio_value_paid')
    order_id = request.args.get('order_id')

    if (order_id) and (status_id) and(paid_id):
        
        db.session.query(Orders).filter(Orders.OrderID == order_id).update({Orders.Status : status_id, Orders.IsPaid : paid_id})
        db.session.commit()
        

        return jsonify({'status' : 'done'})
    return jsonify({'status' : 'error'})


@admin.route("/top_genre")
def top_genre():
    items = db.session.execute('select Name, order_count from (select GenreID, sum(order_details.Quantity) as order_count from order_details, book where book.BookID = order_details.BookID group by GenreID) as genre_count, genre where genre_count.GenreID = genre.GenreID order by order_count desc limit 5;')
    di = dict()
    for k,v in items.fetchall():
        di[k] = v
    
    return jsonify(di)

@admin.route("/sales5days")
def sales5days():
    items = db.session.execute('select DATE(Date), sum(TotalPrice) from orders group by DATE(Date) order by DATE(Date) desc limit 5;')
    di = dict()
    for k,v in items.fetchall():
        di[str(k)] = v
        print(type(k))
    
    return jsonify(di)

@admin.route("/admin_dashboard/book_management")
def book_management():
    form = AddBookForm()

    return render_template('admin/book_management.html', title='Book Management', form=form)