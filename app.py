from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def login():
    return render_template("login.html")


@app.route("/user/dashboard")
def user_dashboard():
    return render_template("dashboard_user.html")

@app.route("/complaint/register")
def complaint_register():
    return render_template("complaint_register.html")

@app.route("/complaints")
def complaints():
    return render_template("complaint_list.html")


@app.route("/org-admin/dashboard")
def org_admin_dashboard():
    return render_template("dashboard_org_admin.html")


@app.route("/department/dashboard")
def department_dashboard():
    return render_template("dashboard_department.html")


@app.route("/support/dashboard")
def support_dashboard():
    return render_template("dashboard_support.html")


@app.route("/super-admin/dashboard")
def superadmin_dashboard():
    return render_template("dashboard_superadmin.html")

@app.route("/payments")
def payments():
    return render_template("payments.html")


@app.route("/analytics")
def analytics():
    return render_template("analytics.html")

@app.route("/register")
def register():
    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
