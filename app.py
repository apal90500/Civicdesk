import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)



BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "change-this-secret")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'civicdesk.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='Pending')
    priority = db.Column(db.String(20), default='Normal')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

with app.app_context():
    db.create_all()



def login_required(f):
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please login first", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper


@app.route("/")
def login():
    if 'user_id' in session:
        return redirect_to_dashboard(session['user_role'])
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        session['user_role'] = user.role
        session['user_department'] = user.department
        flash("Login successful", "success")
        return redirect_to_dashboard(user.role)

    flash("Invalid credentials", "error")
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully")
    return redirect(url_for("login"))


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register_post():
    full_name = request.form.get("full_name")
    email = request.form.get("email")
    role = request.form.get("role")
    department = request.form.get("department")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")

    if password != confirm_password:
        flash("Passwords do not match", "error")
        return redirect(url_for("register"))

    if User.query.filter_by(email=email).first():
        flash("Email already exists", "error")
        return redirect(url_for("register"))

    hashed = generate_password_hash(password)

    new_user = User(
        full_name=full_name,
        email=email,
        password=hashed,
        role=role,
        department=department
    )

    db.session.add(new_user)
    db.session.commit()

    flash("Registration successful")
    return redirect(url_for("login"))



def redirect_to_dashboard(role):
    routes = {
        "End User": "user_dashboard",
        "Organization Admin": "org_admin_dashboard",
        "Department Admin": "department_dashboard",
        "Support Staff": "support_dashboard",
        "Super Admin": "superadmin_dashboard"
    }
    return redirect(url_for(routes.get(role, "user_dashboard")))



@app.route("/user/dashboard")
@login_required
def user_dashboard():
    complaints = Complaint.query.filter_by(user_id=session['user_id']).all()

    total = len(complaints)
    pending = len([c for c in complaints if c.status == "Pending"])
    resolved = len([c for c in complaints if c.status == "Resolved"])

    return render_template("dashboard_user.html",
                           total=total,
                           pending=pending,
                           resolved=resolved,
                           complaints=complaints)



@app.route("/complaint/register")
@login_required
def complaint_register():
    return render_template("complaint_register.html")


@app.route("/complaint/register", methods=["POST"])
@login_required
def complaint_register_post():
    new_complaint = Complaint(
        title=request.form.get("title"),
        description=request.form.get("description"),
        department=request.form.get("department"),
        user_id=session['user_id']
    )

    db.session.add(new_complaint)
    db.session.commit()

    flash("Complaint registered successfully")
    return redirect(url_for("complaints"))


@app.route("/complaints")
@login_required
def complaints():
    user = User.query.get(session['user_id'])

    if user.role == "End User":
        complaint_list = Complaint.query.filter_by(user_id=user.id).all()

    elif user.role == "Department Admin":
        complaint_list = Complaint.query.filter_by(department=user.department).all()

    else:
        complaint_list = Complaint.query.all()

    return render_template("complaint_list.html",
                           complaints=complaint_list,
                           user=user)


@app.route("/complaint/<int:id>/update-status", methods=["POST"])
@login_required
def update_status(id):
    complaint = Complaint.query.get_or_404(id)
    complaint.status = request.form.get("status")
    complaint.updated_at = datetime.utcnow()

    db.session.commit()
    flash("Status updated")
    return redirect(url_for("complaints"))


@app.route("/org-admin/dashboard")
@login_required
def org_admin_dashboard():
    total = Complaint.query.count()
    return render_template("dashboard_org_admin.html", total=total)


@app.route("/department/dashboard")
@login_required
def department_dashboard():
    return render_template("dashboard_department.html")


@app.route("/support/dashboard")
@login_required
def support_dashboard():
    complaints = Complaint.query.order_by(Complaint.created_at.desc()).limit(10)
    return render_template("dashboard_support.html", complaints=complaints)


@app.route("/super-admin/dashboard")
@login_required
def superadmin_dashboard():
    users = User.query.count()
    complaints = Complaint.query.count()
    return render_template("dashboard_superadmin.html",
                           total_users=users,
                           total_complaints=complaints)


@app.route("/payments")
@login_required
def payments():
    return render_template("payments.html")


@app.route("/analytics")
@login_required
def analytics():
    return render_template("analytics.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)