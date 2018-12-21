from flask import Blueprint, render_template






admin = Blueprint('admin', __name__)


@admin.route("/admin/dashboard")
def dashboard():
    return  render_template('dashboard_area/layout.html')