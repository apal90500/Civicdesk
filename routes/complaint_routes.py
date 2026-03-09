from flask import Blueprint, render_template, request, redirect, session, flash
from models.complaint import Complaint
from models.user import User
from models import db
import random

complaint_bp = Blueprint("complaint_bp", __name__)


@complaint_bp.route("/complaints")
def complaints():

    if not session.get("user_id"):
        return redirect("/")

    user = User.query.get(session["user_id"])

    complaint_list = Complaint.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        Complaint.created_at.desc()
    ).all()

    return render_template(
        "complaint_list.html",
        complaints=complaint_list,
        user=user
    )


@complaint_bp.route("/complaint/register", methods=["GET","POST"])
def register_complaint():

    if request.method == "POST":

        title = request.form.get("title")
        description = request.form.get("description")
        department = request.form.get("department")

        
        ticket = "CD-" + str(random.randint(100000,999999))

        complaint = Complaint(
            ticket_id=ticket,
            title=title,
            description=description,
            department=department,
            user_id=session.get("user_id")
        )

        db.session.add(complaint)
        db.session.commit()

        flash("Complaint submitted successfully","success")

        return redirect("/complaints")

    return render_template("complaint_register.html")