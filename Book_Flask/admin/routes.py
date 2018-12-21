from flask import Blueprint, render_template, request
from Book_Flask import db
from Book_Flask.models import User, OrderDetails, Orders , Ispaid, Status, Paymentmethod







admin = Blueprint('admin', __name__)


@admin.route("/admin/dashboard")
def dashboard():
    return  render_template('dashboard_area/layout.html')



@admin.route("/admin/dashboard/order_management")
def order_management():

    page = request.args.get('page',1 , type=int)
    per_page = 10

    items = db.session.query(Orders.OrderID, Orders.Date, User.UserID, User.FirstName, User.LastName, Orders.Address, Orders.Phone, Orders.TotalPrice, Ispaid.NamePaid, Paymentmethod.NamePayment, Status.NameStatus).filter(User.UserID == Orders.UserID).filter(Orders.IsPaid == Ispaid.IsPaidID).filter(Orders.PaymentMethod == Paymentmethod.PaymentMethodID).filter(Orders.Status == Status.StatusID).order_by(Orders.Date.desc()).paginate(page = page, per_page = per_page)

    db.session.close()
    return render_template('dashboard_area/order_management.html', items = items)