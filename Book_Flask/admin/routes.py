from flask import Blueprint, render_template, jsonify
from Book_Flask import db

admin = Blueprint('admin', __name__)


@admin.route("/admin/dashboard")
def dashboard():
    return  render_template('dashboard_area/dashboard_chart.html')

@admin.route("/top_genre")
def top_genre():
    items = db.session.execute('select Name, order_count from (select GenreID, sum(order_details.Quantity) as order_count from order_details, book where book.BookID = order_details.BookID group by GenreID) as genre_count, genre where genre_count.GenreID = genre.GenreID order by order_count desc limit 5;')
    di = dict()
    for k,v in items.fetchall():
        di[k] = v
    return jsonify(di)