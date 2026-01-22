"""
Django models for the student_app.

Models define the structure of your database tables.
Each model class represents a database table, and each attribute represents a field (column).
Django automatically creates SQL CREATE TABLE statements based on these models.
"""

from django.db import models
# models module provides the base Model class and field types


class Student(models.Model):
    """
    Student model represents a student record in the database.
    
    Each field below becomes a column in the student_app_student table.
    """
    
    # CharField for text data with a maximum length
    # first_name stores the student's first name (max 100 characters)
    # null=False means this field cannot be empty in the database
    # blank=False means this field is required in forms
    first_name = models.CharField(max_length=100, null=False, blank=False)
    
    # last_name stores the student's last name
    last_name = models.CharField(max_length=100, null=False, blank=False)
    
    # EmailField is a specialized CharField that validates email format
    # unique=True ensures no two students can have the same email
    email = models.EmailField(unique=True, null=False, blank=False)
    
    # IntegerField stores whole numbers
    # roll_number is a unique identifier for each student
    roll_number = models.IntegerField(unique=True, null=False, blank=False)
    
    # CharField for selecting from predefined choices
    # choices parameter defines what values are allowed
    # max_length must be at least as long as the longest choice value
    # This field limits data to only these specific values
    GRADE_CHOICES = [
        ('A', 'A - Excellent'),
        ('B', 'B - Good'),
        ('C', 'C - Average'),
        ('D', 'D - Below Average'),
        ('F', 'F - Fail'),
    ]
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES, null=False, blank=False)
    
    # IntegerField for the student's age
    age = models.IntegerField(null=False, blank=False)
    
    # DateField stores dates (YYYY-MM-DD format)
    # auto_now_add=True automatically sets the date when the record is created
    # This field is read-only after creation
    date_of_registration = models.DateField(auto_now_add=True)
    
    # DateField stores the student's date of birth
    date_of_birth = models.DateField(null=False, blank=False)
    
    # TextField for longer text content (no character limit)
    # Used for addresses or descriptions
    address = models.TextField(null=False, blank=False)
    
    # CharField for phone numbers
    phone_number = models.CharField(max_length=15, null=False, blank=False)
    
    # BooleanField stores True/False values
    # This tracks whether the student is currently active
    is_active = models.BooleanField(default=True)
    
    # DateTimeField for date and time
    # auto_now=True updates this timestamp every time the record is saved
    # This tracks when the record was last modified
    updated_at = models.DateTimeField(auto_now=True)

    # Meta class provides metadata options for the model
    class Meta:
        # verbose_name sets the human-readable name for the model (singular)
        verbose_name = 'Student'
        # verbose_name_plural sets the plural form (used in admin)
        verbose_name_plural = 'Students'
        # ordering specifies the default order for queries
        # '-date_of_registration' means newest first (- means descending)
        ordering = ['-date_of_registration']

    # __str__ method defines how the object appears as a string
    # This is used in admin panel, forms, and Django shell
    # Returns the student's full name
    def __str__(self):
        return f"{self.first_name} {self.last_name} (Roll: {self.roll_number})"
