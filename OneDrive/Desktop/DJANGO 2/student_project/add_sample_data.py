#!/usr/bin/env python
"""
Script to add sample student data to the database
and create a superuser for admin access.
"""

import os
import django
from datetime import date

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_project.settings')
django.setup()

from django.contrib.auth.models import User
from student_app.models import Student

# Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("✓ Superuser 'admin' created successfully (password: admin123)")
else:
    print("✓ Superuser 'admin' already exists")

# Sample student data
students_data = [
    {
        'first_name': 'Rajesh',
        'last_name': 'Kumar',
        'email': 'rajesh@example.com',
        'roll_number': 101,
        'grade': 'A',
        'age': 20,
        'date_of_birth': date(2004, 5, 15),
        'address': '123 Main Street, Delhi',
        'phone_number': '9876543210',
        'is_active': True
    },
    {
        'first_name': 'Priya',
        'last_name': 'Singh',
        'email': 'priya@example.com',
        'roll_number': 102,
        'grade': 'A',
        'age': 19,
        'date_of_birth': date(2005, 8, 22),
        'address': '456 Park Avenue, Mumbai',
        'phone_number': '8765432109',
        'is_active': True
    },
    {
        'first_name': 'Amit',
        'last_name': 'Patel',
        'email': 'amit@example.com',
        'roll_number': 103,
        'grade': 'B',
        'age': 21,
        'date_of_birth': date(2003, 3, 10),
        'address': '789 Oak Road, Bangalore',
        'phone_number': '7654321098',
        'is_active': True
    },
    {
        'first_name': 'Neha',
        'last_name': 'Sharma',
        'email': 'neha@example.com',
        'roll_number': 104,
        'grade': 'B',
        'age': 20,
        'date_of_birth': date(2004, 1, 5),
        'address': '321 Elm Street, Pune',
        'phone_number': '6543210987',
        'is_active': True
    },
    {
        'first_name': 'Rahul',
        'last_name': 'Verma',
        'email': 'rahul@example.com',
        'roll_number': 105,
        'grade': 'C',
        'age': 22,
        'date_of_birth': date(2002, 12, 18),
        'address': '654 Pine Lane, Hyderabad',
        'phone_number': '5432109876',
        'is_active': True
    }
]

# Add students to database
count = 0
for student_data in students_data:
    if not Student.objects.filter(roll_number=student_data['roll_number']).exists():
        Student.objects.create(**student_data)
        count += 1

print(f"✓ {count} sample students added successfully")
print(f"✓ Total students in database: {Student.objects.count()}")
print("\n" + "="*60)
print("SUCCESS: Database setup complete!")
print("="*60)
print(f"Admin credentials: username='admin', password='admin123'")
print(f"Visit: http://127.0.0.1:8000/admin/ to login")
print("="*60)
