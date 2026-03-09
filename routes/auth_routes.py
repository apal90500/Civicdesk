from flask import Blueprint, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from models import db

auth_bp = Blueprint("auth_bp", __name__)




@auth_bp.route("/")
def home():
    return render_template("login.html")




@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("User not found", "error")
            return redirect("/")

        if not check_password_hash(user.password, password):
            flash("Incorrect password", "error")
            return redirect("/")

        session["user_id"] = user.id
        session["user_name"] = user.full_name
        session["user_role"] = user.role

        flash("Login successful", "success")

        return redirect("/complaints")

    return render_template("login.html")



@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password = request.form.get("password")

        # check if email exists
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already registered", "error")
            return redirect("/register")

        hashed_password = generate_password_hash(password)

        new_user = User(
            full_name=full_name,
            email=email,
            password=hashed_password,
            role="End User",        # FIXED
            department="General"
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully", "success")

        return redirect("/")

    return render_template("register.html")



@auth_bp.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully", "success")

    return redirect("/")