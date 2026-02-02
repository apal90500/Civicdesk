"""
Script to create test users for CivicDesk
Run this to populate the database with sample users
"""
from app import app, db, User
from werkzeug.security import generate_password_hash

def create_test_users():
    with app.app_context():
        # Check if users already exist
        if User.query.count() > 0:
            print(f"Database already has {User.query.count()} users.")
            print("Skipping user creation.")
            return
        
        # All departments in the system
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
        
        # Create test users
        users = [
            {
                'full_name': 'John Doe',
                'email': 'user@example.com',
                'password': 'password123',
                'role': 'End User',
                'department': None
            },
            {
                'full_name': 'Org Admin',
                'email': 'admin@example.com',
                'password': 'password123',
                'role': 'Organization Admin',
                'department': None
            },
            {
                'full_name': 'Support Staff',
                'email': 'support@example.com',
                'password': 'password123',
                'role': 'Support Staff',
                'department': None
            }
        ]
        
        # Create a Department Admin for each department
        for dept in departments:
            # Create email from department name (e.g., "IT Systems" -> "it@example.com")
            email_prefix = dept.lower().replace(' ', '').replace('/', '')[:10]
            users.append({
                'full_name': f'{dept} Admin',
                'email': f'{email_prefix}@example.com',
                'password': 'password123',
                'role': 'Department Admin',
                'department': dept
            })
        
        for user_data in users:
            user = User(
                full_name=user_data['full_name'],
                email=user_data['email'],
                password=generate_password_hash(user_data['password']),
                role=user_data['role'],
                department=user_data['department']
            )
            db.session.add(user)
        
        db.session.commit()
        print("✅ Test users created successfully!")
        print("\nYou can now login with:")
        print("=" * 50)
        for user_data in users:
            print(f"Email: {user_data['email']}")
            print(f"Password: {user_data['password']}")
            print(f"Role: {user_data['role']}")
            if user_data['department']:
                print(f"Department: {user_data['department']}")
            print("-" * 50)

if __name__ == '__main__':
    create_test_users()
