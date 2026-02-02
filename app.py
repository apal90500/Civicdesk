from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///civicdesk.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # End User, Organization Admin, Department Admin, Support Staff
    department = db.Column(db.String(100))  # Department assignment for department users
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    complaints = db.relationship('Complaint', backref='user', lazy=True, foreign_keys='Complaint.user_id')

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='Pending')  # Pending, In Progress, Resolved, Closed
    priority = db.Column(db.String(20), default='Normal')  # Normal, High, Urgent
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Initialize database
with app.app_context():
    db.create_all()

# Helper function to check login
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route("/")
def login():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return redirect_to_dashboard(user.role)
    return render_template("login.html")

@app.route("/login", methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    
    user = User.query.filter_by(email=email).first()
    
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        session['user_name'] = user.full_name
        session['user_role'] = user.role
        session['user_department'] = user.department
        flash('Login successful!', 'success')
        return redirect_to_dashboard(user.role)
    else:
        flash('Invalid email or password', 'error')
        return redirect(url_for('login'))

@app.route("/logout")
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register", methods=['POST'])
def register_post():
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    role = request.form.get('role')
    department = request.form.get('department', None)
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    
    if password != confirm_password:
        flash('Passwords do not match', 'error')
        return redirect(url_for('register'))
    
    if User.query.filter_by(email=email).first():
        flash('Email already registered', 'error')
        return redirect(url_for('register'))
    
    hashed_password = generate_password_hash(password)
    new_user = User(
        full_name=full_name,
        email=email,
        password=hashed_password,
        role=role,
        department=department
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    flash('Registration successful! Please login.', 'success')
    return redirect(url_for('login'))

def redirect_to_dashboard(role):
    if role == 'End User':
        return redirect(url_for('user_dashboard'))
    elif role == 'Organization Admin':
        return redirect(url_for('org_admin_dashboard'))
    elif role == 'Department Admin':
        return redirect(url_for('department_dashboard'))
    elif role == 'Support Staff':
        return redirect(url_for('support_dashboard'))
    elif role == 'Super Admin':
        return redirect(url_for('superadmin_dashboard'))
    else:
        return redirect(url_for('user_dashboard'))

@app.route("/user/dashboard")
@login_required
def user_dashboard():
    user = User.query.get(session['user_id'])
    user_complaints = Complaint.query.filter_by(user_id=user.id).all()
    
    total_complaints = len(user_complaints)
    pending = len([c for c in user_complaints if c.status == 'Pending'])
    resolved = len([c for c in user_complaints if c.status == 'Resolved'])
    
    return render_template("dashboard_user.html", 
                         total=total_complaints, 
                         pending=pending, 
                         resolved=resolved,
                         complaints=user_complaints)

@app.route("/complaint/register")
@login_required
def complaint_register():
    return render_template("complaint_register.html")

@app.route("/complaint/register", methods=['POST'])
@login_required
def complaint_register_post():
    title = request.form.get('title')
    department = request.form.get('department')
    description = request.form.get('description')
    
    new_complaint = Complaint(
        title=title,
        description=description,
        department=department,
        user_id=session['user_id']
    )
    
    db.session.add(new_complaint)
    db.session.commit()
    
    flash('Complaint registered successfully!', 'success')
    return redirect(url_for('complaints'))

@app.route("/complaints")
@login_required
def complaints():
    user = User.query.get(session['user_id'])
    
    if user.role == 'End User':
        # End users see only their own complaints
        complaint_list = Complaint.query.filter_by(user_id=user.id).order_by(Complaint.created_at.desc()).all()
    elif user.role == 'Department Admin':
        # Department admins see complaints for their department only
        complaint_list = Complaint.query.filter_by(department=user.department).order_by(Complaint.created_at.desc()).all()
    elif user.role in ['Organization Admin', 'Support Staff', 'Super Admin']:
        # Admins see all complaints
        complaint_list = Complaint.query.order_by(Complaint.created_at.desc()).all()
    else:
        complaint_list = []
    
    return render_template("complaint_list.html", complaints=complaint_list, user=user)

@app.route("/complaint/<int:complaint_id>/update-status", methods=['POST'])
@login_required
def update_complaint_status(complaint_id):
    complaint = Complaint.query.get_or_404(complaint_id)
    new_status = request.form.get('status')
    
    user = User.query.get(session['user_id'])
    
    # Only department admins, org admins, and support staff can update status
    if user.role in ['Department Admin', 'Organization Admin', 'Support Staff', 'Super Admin']:
        complaint.status = new_status
        complaint.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Complaint status updated!', 'success')
    else:
        flash('You do not have permission to update complaint status', 'error')
    
    return redirect(url_for('complaints'))

@app.route("/org-admin/dashboard")
@login_required
def org_admin_dashboard():
    total_complaints = Complaint.query.count()
    pending = Complaint.query.filter_by(status='Pending').count()
    in_progress = Complaint.query.filter_by(status='In Progress').count()
    resolved = Complaint.query.filter_by(status='Resolved').count()
    
    # Department-wise breakdown
    departments = db.session.query(Complaint.department, db.func.count(Complaint.id)).group_by(Complaint.department).all()
    
    return render_template("dashboard_org_admin.html",
                         total=total_complaints,
                         pending=pending,
                         in_progress=in_progress,
                         resolved=resolved,
                         departments=departments)

@app.route("/department/dashboard")
@login_required
def department_dashboard():
    user = User.query.get(session['user_id'])
    
    if not user.department:
        flash('No department assigned to your account', 'error')
        return redirect(url_for('login'))
    
    # Get complaints for this department
    dept_complaints = Complaint.query.filter_by(department=user.department).all()
    
    total = len(dept_complaints)
    pending = len([c for c in dept_complaints if c.status == 'Pending'])
    in_progress = len([c for c in dept_complaints if c.status == 'In Progress'])
    resolved = len([c for c in dept_complaints if c.status == 'Resolved'])
    
    return render_template("dashboard_department.html",
                         department=user.department,
                         total=total,
                         pending=pending,
                         in_progress=in_progress,
                         resolved=resolved,
                         complaints=dept_complaints)

@app.route("/support/dashboard")
@login_required
def support_dashboard():
    recent_complaints = Complaint.query.order_by(Complaint.created_at.desc()).limit(10).all()
    return render_template("dashboard_support.html", complaints=recent_complaints)

@app.route("/super-admin/dashboard")
@login_required
def superadmin_dashboard():
    total_users = User.query.count()
    total_complaints = Complaint.query.count()
    
    # Role-wise user count
    role_counts = db.session.query(User.role, db.func.count(User.id)).group_by(User.role).all()
    
    return render_template("dashboard_superadmin.html",
                         total_users=total_users,
                         total_complaints=total_complaints,
                         role_counts=role_counts)

@app.route("/payments")
@login_required
def payments():
    return render_template("payments.html")

@app.route("/analytics")
@login_required
def analytics():
    return render_template("analytics.html")

if __name__ == "__main__":
    app.run(debug=True)
