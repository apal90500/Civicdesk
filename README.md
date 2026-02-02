# CivicDesk - Universal Complaint Management System

## Overview
CivicDesk is a Flask-based complaint management system that allows organizations to manage complaints with department-based assignment and role-based access control.

## Features

### Department-Based Complaint Assignment
- When a complaint is registered, it is assigned to a specific department
- Department Admin users only see complaints assigned to their department
- This ensures complaints are routed to the right people for resolution

### Role-Based Access Control

1. **End User**
   - Can register complaints
   - View their own complaints
   - Track complaint status

2. **Department Admin**
   - Assigned to a specific department (Education, IT, Infrastructure, etc.)
   - Only sees complaints for their department
   - Can update complaint status (Pending → In Progress → Resolved → Closed)
   
3. **Organization Admin**
   - Views all complaints across all departments
   - Can see department-wise breakdown
   - Monitors overall complaint resolution

4. **Support Staff**
   - Views all complaints
   - Assists users and escalates issues
   - Can update complaint status

5. **Super Admin**
   - Full platform access
   - Views user statistics and role distribution
   - Platform-level management

### Complaint Workflow

1. **User Registration**: Users register with a role. Department Admin users must select their department.
2. **Complaint Registration**: Users submit complaints and select the relevant department.
3. **Department Assignment**: Complaints are automatically visible to Department Admins of that department.
4. **Status Management**: Department Admins can update complaint status through the dropdown.
5. **Resolution Tracking**: Users can track their complaint status in real-time.

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```

The application will be available at: `http://127.0.0.1:5000`

### 3. First-Time Setup
The database will be automatically created when you first run the application.

## Usage Guide

### Creating Users

1. **Create a Department Admin**:
   - Go to `/register`
   - Fill in details
   - Select role: "Department Admin"
   - Select department: e.g., "IT Systems"
   - This user will only see IT Systems complaints

2. **Create an End User**:
   - Select role: "End User"
   - No department selection needed
   - Can register and track complaints

### Registering Complaints

1. Login as End User
2. Click "Register New Complaint"
3. Enter title, select department, add description
4. Submit complaint
5. Complaint is now visible to:
   - The user who created it
   - Department Admin for that department
   - Organization Admins and Support Staff

### Managing Complaints (Department Admin)

1. Login as Department Admin
2. Dashboard shows only complaints for your department
3. View complaint details
4. Update status using dropdown (Pending → In Progress → Resolved)
5. Track department performance metrics

## Database Schema

### User Table
- id, full_name, email, password, role, department, created_at

### Complaint Table
- id, title, description, department, status, priority, user_id, assigned_to, created_at, updated_at

## Security Features

- Password hashing using Werkzeug
- Session-based authentication
- Role-based access control
- Login required decorators

## Technologies Used

- **Backend**: Flask, SQLAlchemy
- **Database**: SQLite
- **Frontend**: Tailwind CSS
- **Authentication**: Flask Sessions with Werkzeug password hashing

## Department List

- Education
- Residential Facilities
- Infrastructure
- Electricity
- Water
- IT Systems
- Transport
- Administration
- Staff Behaviour
- Security
- Health
- Finance
- General Complaint

## Future Enhancements

- Email notifications
- File attachments for complaints
- Advanced analytics and reporting
- Export complaints to PDF/Excel
- Real-time chat support
- Mobile app integration
