# Employee Leave Management System

A Django + Django REST Framework web application for managing employees and employee leave requests with separate Admin and Employee login flows.

## Features

- Separate Admin and Employee login
- Admin dashboard with employee and leave counts
- Admin employee management:
  - Add employees
  - Update employees
  - Delete employees
  - Create employee login credentials
- Employee leave management:
  - Employees can apply for leave
  - Employees can view only their own leave applications
  - Employees can edit/delete only pending leave requests
- Admin leave approval flow:
  - View all leave applications
  - Update leave status to Pending, Approved, or Rejected
- CSRF-protected AJAX requests
- MySQL database support

## Tech Stack

- Python
- Django 5.2.5
- Django REST Framework 3.16.0
- MySQL
- Bootstrap 5
- JavaScript Fetch API

## Project Structure

```text
EmployeeLeaveManagement/
|-- EmployeeLeaveManagement/
|   |-- settings.py
|   |-- urls.py
|   |-- asgi.py
|   `-- wsgi.py
|-- employee/
|   |-- migrations/
|   |-- static/
|   |   |-- css/
|   |   `-- js/
|   |-- templates/
|   |-- admin.py
|   |-- models.py
|   |-- serializers.py
|   |-- urls.py
|   `-- views.py
|-- manage.py
|-- requirements.txt
`-- README.md
```

## Main Pages

```text
/login/       Login page
/logout/      Logout
/dashboard/   Admin dashboard
/employees/   Admin employee management
/leaves/      Leave management
/admin/       Django admin panel
```

## API Endpoints

```text
GET    /api/dashboard/
GET    /api/employees/
POST   /api/employees/
GET    /api/employees/<id>/
PUT    /api/employees/<id>/
DELETE /api/employees/<id>/
GET    /api/leaves/
POST   /api/leaves/
GET    /api/leaves/<id>/
PUT    /api/leaves/<id>/
DELETE /api/leaves/<id>/
```

## Setup Instructions

1. Clone the repository:

```bash
git clone https://github.com/BhagyodayaBamgonda/Django_Assignment.git
cd Django_Assignment
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure MySQL database in `EmployeeLeaveManagement/settings.py`.

Use your own local database credentials. Do not commit real passwords to GitHub.

5. Create the database in MySQL:

```sql
CREATE DATABASE employee_leave_db;
```

6. Run migrations:

```bash
python manage.py migrate
```

7. Create an admin user:

```bash
python manage.py createsuperuser
```

8. Start the server:

```bash
python manage.py runserver
```

9. Open the app:

```text
http://127.0.0.1:8000/login/
```

## Login Flow

### Admin

Create an admin using:

```bash
python manage.py createsuperuser
```

Then login as `Admin` from `/login/`.

Admin can:

- View dashboard
- Add/update/delete employees
- Create employee usernames and passwords
- View all leave applications
- Approve or reject leaves

### Employee

An employee login is created when Admin adds an employee from `/employees/`.

Employee can:

- Login as `Employee`
- Apply for leave
- View own leave applications
- Edit/delete pending leave requests

Employee cannot approve or reject leave.

## Notes

- Leave status is controlled by Admin only.
- New leave applications are created with `Pending` status by default.
- Employee delete also removes the linked login user.
- CSRF tokens are included in the base template and sent with all mutating JavaScript requests.

## Useful Commands

```bash
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
