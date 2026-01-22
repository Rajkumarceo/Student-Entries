# Quick Start Guide - Django Student Management System

## 30-Minute Setup

### Step 1: Navigate to Project (1 min)
```bash
cd "c:\Users\Rajkumar\OneDrive\Desktop\DJANGO 2\student_project"
```

### Step 2: Create Virtual Environment (2 min)
```bash
python -m venv env
```

### Step 3: Activate Virtual Environment (1 min)
**Windows:**
```bash
env\Scripts\activate
```

**Mac/Linux:**
```bash
source env/bin/activate
```

### Step 4: Install Dependencies (5 min)
```bash
pip install Django==4.2.0
```

### Step 5: Create Database (2 min)
```bash
python manage.py migrate
```

This creates `db.sqlite3` file.

### Step 6: Create Admin Account (2 min)
```bash
python manage.py createsuperuser
```

When prompted:
- Username: `admin`
- Email: `admin@example.com`
- Password: `admin123` (or your choice)

### Step 7: Start Server (2 min)
```bash
python manage.py runserver
```

You'll see:
```
Starting development server at http://127.0.0.1:8000/
```

### Step 8: Access the Application (1 min)

Open your browser:

| URL | Purpose |
|-----|---------|
| http://localhost:8000/ | Student List |
| http://localhost:8000/create/ | Create Student |
| http://localhost:8000/admin/ | Admin Panel |

---

## Quick Database Operations

### Add Sample Data

**Option 1: Via Web Form**
1. Go to http://localhost:8000/create/
2. Fill in form:
   - First Name: John
   - Last Name: Doe
   - Email: john@example.com
   - Roll Number: 1
   - Grade: A
   - Age: 20
   - Date of Birth: 2004-01-01
   - Address: 123 Main St
   - Phone: 1234567890
3. Click "Create Student"

**Option 2: Via Django Shell**
```bash
python manage.py shell
```

```python
from student_app.models import Student

# Create 3 sample students
students_data = [
    {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john@example.com',
        'roll_number': 1,
        'grade': 'A',
        'age': 20,
        'date_of_birth': '2004-01-01',
        'address': '123 Main St',
        'phone_number': '1234567890'
    },
    {
        'first_name': 'Jane',
        'last_name': 'Smith',
        'email': 'jane@example.com',
        'roll_number': 2,
        'grade': 'B',
        'age': 21,
        'date_of_birth': '2003-05-15',
        'address': '456 Oak Ave',
        'phone_number': '0987654321'
    },
    {
        'first_name': 'Bob',
        'last_name': 'Wilson',
        'email': 'bob@example.com',
        'roll_number': 3,
        'grade': 'A',
        'age': 20,
        'date_of_birth': '2004-03-20',
        'address': '789 Pine Rd',
        'phone_number': '5555555555'
    }
]

for data in students_data:
    Student.objects.create(**data)

# Verify
print(f"Total students: {Student.objects.count()}")
```

---

## File Structure Quick Reference

```
student_project/                    # Project folder
│
├── manage.py                        # Management script
├── db.sqlite3                       # Database (auto-created)
├── requirements.txt                 # Dependencies
│
├── student_project/                 # Configuration folder
│   ├── settings.py                  # Project settings
│   ├── urls.py                      # Main URL routing
│   └── ...
│
├── student_app/                     # Student app
│   ├── models.py                    # Database models
│   ├── views.py                     # View logic
│   ├── forms.py                     # Forms
│   ├── admin.py                     # Admin setup
│   ├── urls.py                      # App URLs
│   └── templates/
│       └── student_app/
│           ├── student_list.html    # List page
│           ├── student_detail.html  # Detail page
│           ├── student_form.html    # Create/Edit form
│           └── student_confirm_delete.html
│
└── templates/                       # Global templates
    └── base.html                    # Base layout
```

---

## Common Tasks

### View All Students
```bash
# Method 1: Web Interface
# Go to http://localhost:8000/

# Method 2: Django Shell
python manage.py shell
>>> from student_app.models import Student
>>> Student.objects.all()
```

### Search for Student
```bash
# Web: Use search box on student list page

# Shell:
>>> Student.objects.filter(first_name='John')
>>> Student.objects.get(roll_number=1)
```

### Update Student
```bash
# Web: Click Edit on student detail page

# Shell:
>>> student = Student.objects.get(roll_number=1)
>>> student.grade = 'B'
>>> student.save()
```

### Delete Student
```bash
# Web: Click Delete on student detail page

# Shell:
>>> Student.objects.get(roll_number=1).delete()
```

### Check Student Count
```bash
python manage.py shell
>>> from student_app.models import Student
>>> Student.objects.count()
```

---

## Troubleshooting

### Error: "Port 8000 already in use"
```bash
python manage.py runserver 8001
```
Then go to http://localhost:8001/

### Error: "No database"
```bash
python manage.py migrate
```

### Error: "Table doesn't exist"
```bash
python manage.py migrate
python manage.py createsuperuser
```

### Error: "Module not found"
```bash
pip install -r requirements.txt
```

### Forgot Admin Password
```bash
python manage.py changepassword admin
```

---

## Testing the Application

### Create Student Scenario
1. Go to http://localhost:8000/
2. Click "Add Student" button
3. Fill in form with test data
4. Click "Create Student"
5. You should see confirmation message

### View Student Scenario
1. From student list, click on a student name
2. See all student details
3. Note the Edit and Delete buttons

### Search Scenario
1. Go to http://localhost:8000/
2. Type name/email in search box
3. Click Search
4. See filtered results

### Admin Scenario
1. Go to http://localhost:8000/admin/
2. Login with admin credentials
3. Click "Students"
4. Try filtering, searching, adding records

---

## Project URLs Map

```
Home/List          http://localhost:8000/
Create Student     http://localhost:8000/create/
View Student       http://localhost:8000/student/1/
Edit Student       http://localhost:8000/student/1/edit/
Delete Student     http://localhost:8000/student/1/delete/
Admin Panel        http://localhost:8000/admin/
```

Replace `1` with actual student ID.

---

## Command Reference

```bash
# Start server
python manage.py runserver

# Open Django shell
python manage.py shell

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Change admin password
python manage.py changepassword admin

# Run tests
python manage.py test

# Delete all data (dangerous!)
python manage.py flush

# Export data to JSON
python manage.py dumpdata > backup.json

# Import data from JSON
python manage.py loaddata backup.json

# View SQL query
python manage.py sqlmigrate student_app 0001
```

---

## Next Steps

After understanding the basics:

1. **Customize Templates**: Edit HTML files in `templates/` folder
2. **Add More Fields**: Modify `models.py` and run migrations
3. **Change Styling**: Modify CSS in templates
4. **Add Authentication**: Use Django's `User` model
5. **Add Relationships**: Link students to classes/courses
6. **Deploy to Server**: Use Gunicorn, Nginx, Heroku, AWS, etc.

---

## Important Notes

⚠️ **Security:**
- Change `SECRET_KEY` in `settings.py` before deployment
- Set `DEBUG = False` for production
- Use strong passwords
- Keep Django updated

✅ **Best Practices:**
- Use virtual environment
- Keep sensitive data in environment variables
- Write tests for your code
- Use version control (Git)
- Comment your code

🔧 **Maintenance:**
- Backup database regularly
- Monitor server logs
- Keep dependencies updated
- Test before deploying

---

## Help and Resources

### Official Documentation
- Django: https://docs.djangoproject.com/
- Python: https://docs.python.org/
- Bootstrap: https://getbootstrap.com/

### Common Issues
- Check error message in terminal
- Look at Django logs
- Review code comments in files
- Check admin panel for data issues

### Getting Help
1. Read error messages carefully
2. Check Django documentation
3. Use Django shell to test code
4. Check admin panel for data issues
5. Review browser console for JavaScript errors

---

## You're All Set! 🎉

The Django Student Management System is ready to use!

**What You Can Do:**
✅ Create student records
✅ View student details
✅ Search for students
✅ Update student information
✅ Delete student records
✅ Manage via admin panel

**Happy Learning!** 📚
