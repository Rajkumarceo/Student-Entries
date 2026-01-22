"""
This file is used by Django to add tests for this app.
Tests help ensure your code works correctly.

Example test:
    def test_student_creation(self):
        student = Student.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            roll_number=1,
            grade='A',
            age=20,
            date_of_birth='2004-01-01',
            address='123 Main St',
            phone_number='1234567890'
        )
        self.assertEqual(student.first_name, 'John')
"""

from django.test import TestCase
from .models import Student


class StudentModelTest(TestCase):
    """
    Test cases for the Student model.
    """
    
    def setUp(self):
        """
        setUp is called before each test method.
        Create test data that will be used in tests.
        """
        self.student = Student.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            roll_number=1,
            grade='A',
            age=20,
            date_of_birth='2004-01-01',
            address='123 Main St',
            phone_number='1234567890'
        )
    
    def test_student_creation(self):
        """
        Test that a student can be created with valid data.
        """
        # Verify the student was created
        self.assertTrue(Student.objects.filter(roll_number=1).exists())
    
    def test_student_string_representation(self):
        """
        Test the __str__ method of Student model.
        """
        expected_str = 'John Doe (Roll: 1)'
        self.assertEqual(str(self.student), expected_str)
