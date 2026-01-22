# README.md - Student Management System Documentation

# Student Management System

A complete Django web application for managing student records with Create, Read, Update, and Delete (CRUD) operations.

## Features

- **Student Data Management**: Create, view, update, and delete student records
- **Search and Filter**: Search students by name, email, or roll number
- **Form Validation**: Client-side and server-side validation
- **Responsive Design**: Mobile-friendly interface using Bootstrap
- **Admin Panel**: Django admin interface for direct database management
- **Data Validation**: Ensures data integrity with custom validators
- **Status Tracking**: Track active/inactive student status
- **Academic Records**: Manage grades and academic information

## Project Structure

```
student_project/
├── manage.py                           # Django management script
├── requirements.txt                    # Python dependencies
├── db.sqlite3                          # SQLite database (auto-created)
│
├── student_project/                    # Project configuration folder
│   ├── __init__.py
│   ├── settings.py                     # Project settings
│   ├── urls.py                         # Main URL configuration
│   ├── asgi.py                         # ASGI config (async)
│   └── wsgi.py                         # WSGI config (production)
│
├── student_app/                        # Student app folder
│   ├── migrations/                     # Database migration files
│   │   └── __init__.py
│   ├── templates/                      # HTML templates
│   │   ├── base.html                   # Base template
│   │   └── student_app/
│   │       ├── student_list.html       # Student list page
│   │       ├── student_detail.html     # Student detail page
│   │       ├── student_form.html       # Create/edit form
│   │       └── student_confirm_delete.html  # Delete confirmation
│   ├── static/                         # Static files (CSS, JS, images)
│   ├── __init__.py
│   ├── admin.py                        # Admin configuration
│   ├── apps.py                         # App configuration
│   ├── forms.py                        # Django forms
│   ├── models.py                       # Data models
│   ├── tests.py                        # Unit tests
│   ├── urls.py                         # App URL configuration
│   └── views.py                        # View functions/classes
│
└── templates/                          # Project-level templates
    └── home.html
```

## Installation and Setup

### Step 1: Install Python
Make sure you have Python 3.8 or higher installed.

### Step 2: Create Virtual Environment
```bash
python -m venv env
```

### Step 3: Activate Virtual Environment
**On Windows:**
```bash
env\Scripts\activate
```

**On Mac/Linux:**
```bash
source env/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Apply Migrations
```bash
python manage.py migrate
```

This creates the SQLite database and tables.

### Step 6: Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```

Enter:
- Username: admin
- Email: admin@example.com
- Password: (choose a secure password)

### Step 7: Run Development Server
```bash
python manage.py runserver
```

The server will start at `http://localhost:8000/`

## Usage

### Accessing the Application

1. **Student List Page**: http://localhost:8000/
2. **Create Student**: http://localhost:8000/create/
3. **View Student**: http://localhost:8000/student/1/
4. **Edit Student**: http://localhost:8000/student/1/edit/
5. **Delete Student**: http://localhost:8000/student/1/delete/
6. **Admin Panel**: http://localhost:8000/admin/

### Django Admin Panel

Log in with your superuser credentials to:
- Manage all student records
- Filter and search students
- Export data
- Perform bulk operations

## Database Fields

### Student Model

| Field | Type | Description |
|-------|------|-------------|
| first_name | CharField | Student's first name (max 100 chars) |
| last_name | CharField | Student's last name (max 100 chars) |
| email | EmailField | Student's email (unique) |
| roll_number | IntegerField | Unique roll number |
| grade | CharField | Grade (A, B, C, D, F) |
| age | IntegerField | Student's age |
| date_of_birth | DateField | Student's birth date |
| address | TextField | Student's address |
| phone_number | CharField | Contact phone (max 15 chars) |
| is_active | BooleanField | Active status (default: True) |
| date_of_registration | DateField | Auto-set on creation |
| updated_at | DateTimeField | Auto-updated on modification |

## Management Commands

```bash
# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Change superuser password
python manage.py changepassword admin

# Drop all data and recreate database
python manage.py flush

# Access Django shell (Python REPL with Django context)
python manage.py shell

# Run tests
python manage.py test

# Collect static files (for production)
python manage.py collectstatic
```

## Example Shell Commands

```bash
# Open Django shell
python manage.py shell

# Create a student
>>> from student_app.models import Student
>>> student = Student.objects.create(
...     first_name='John',
...     last_name='Doe',
...     email='john@example.com',
...     roll_number=1,
...     grade='A',
...     age=20,
...     date_of_birth='2004-01-01',
...     address='123 Main St',
...     phone_number='1234567890'
... )

# Query students
>>> students = Student.objects.all()
>>> students.filter(grade='A')
>>> students.get(roll_number=1)

# Update a student
>>> student = Student.objects.get(roll_number=1)
>>> student.grade = 'B'
>>> student.save()

# Delete a student
>>> student.delete()
```

## Customization

### Adding More Fields

Edit `student_app/models.py`:
```python
class Student(models.Model):
    # ... existing fields ...
    new_field = models.CharField(max_length=100)
```

Then:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Changing Styling

Edit `student_app/templates/base.html` to modify:
- Bootstrap CSS classes
- Custom CSS styles
- Color schemes
- Layout

### Adding More Features

1. Create new views in `student_app/views.py`
2. Add new URLs in `student_app/urls.py`
3. Create new templates in `student_app/templates/`

## Troubleshooting

**Port Already in Use**
```bash
python manage.py runserver 8001
```

**Database Errors**
```bash
python manage.py migrate --run-syncdb
```

**Missing Static Files**
```bash
python manage.py collectstatic --noinput
```

## Security Notes

- Change `SECRET_KEY` in `settings.py` for production
- Set `DEBUG = False` in production
- Use environment variables for sensitive data
- Use HTTPS in production
- Keep Django updated
- Use strong passwords

## Performance Tips

- Use `select_related()` and `prefetch_related()` for queries
- Add database indexes for frequently searched fields
- Implement pagination for large datasets
- Use caching for expensive queries
- Optimize static files

## Production Deployment

For production, consider:
1. **Web Server**: Gunicorn, uWSGI
2. **Database**: PostgreSQL, MySQL
3. **Static Files**: Nginx, CloudFront
4. **Security**: SSL/TLS, CSRF protection
5. **Monitoring**: Error tracking, logging

## Testing

```bash
# Run all tests
python manage.py test

# Run specific test
python manage.py test student_app.tests.StudentModelTest

# Run with verbose output
python manage.py test --verbosity=2
```

## License

This project is open source and available for educational purposes.

## Support

For issues or questions:
1. Check Django documentation: https://docs.djangoproject.com/
2. Review code comments
3. Check the admin panel for data issues
4. Review error messages in console

---

**Happy Learning!**
