from flask import Blueprint, render_template
from models.user import User
from models.complaint import Complaint

admin_bp = Blueprint("admin_bp", __name__)


@admin_bp.route("/admin/dashboard")
def admin_dashboard():

    total_users = User.query.count()

    total_complaints = Complaint.query.count()

    return render_template(
        "dashboard_superadmin.html",
        total_users=total_users,
        total_complaints=total_complaints
    )