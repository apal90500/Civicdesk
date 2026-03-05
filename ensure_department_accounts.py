from app import app, db, User
from werkzeug.security import generate_password_hash


def build_email(department: str) -> str:
    return f"{department.lower().replace(' ', '').replace('/', '')[:10]}@example.com"


def ensure_department_accounts() -> None:
    departments = [
        'Education',
        'Residential Facilities',
        'Infrastructure',
        'Electricity',
        'Water',
        'IT Systems',
        'Transport',
        'Administration',
        'Staff Behaviour',
        'Security',
        'Health',
        'Finance',
        'General Complaint'
    ]

    with app.app_context():
        created = []
        existing = []

        for department in departments:
            email = build_email(department)
            user = User.query.filter_by(email=email).first()

            if user:
                existing.append((email, department))
                if user.role != 'Department Admin' or user.department != department:
                    user.role = 'Department Admin'
                    user.department = department
                continue

            new_user = User(
                full_name=f"{department} Admin",
                email=email,
                password=generate_password_hash('password123'),
                role='Department Admin',
                department=department
            )
            db.session.add(new_user)
            created.append((email, department))

        db.session.commit()

    print("Department Admin account status")
    print("=" * 40)
    print(f"Created: {len(created)}")
    print(f"Already existed: {len(existing)}")
    print("\nLogin credentials for all departments:")
    print("Password: password123")
    print("-" * 40)
    for department in departments:
        print(f"{department}: {build_email(department)}")


if __name__ == '__main__':
    ensure_department_accounts()
