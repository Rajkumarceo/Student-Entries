"""
Django admin configuration for the student_app.

This file registers models with Django's admin panel,
allowing you to create, read, update, and delete student records
through a user-friendly web interface.
"""

from django.contrib import admin
# admin module provides the admin site functionality

from .models import Student
# Import the Student model we defined in models.py


# The @admin.register decorator registers the StudentAdmin class with the admin site
# It's equivalent to: admin.site.register(Student, StudentAdmin)
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """
    StudentAdmin customizes how the Student model appears in the Django admin panel.
    """
    
    # list_display specifies which fields to show in the student list view
    # These are the columns you see when viewing all students
    list_display = [
        'roll_number',           # First column: Roll number
        'first_name',            # Second column: First name
        'last_name',             # Third column: Last name
        'email',                 # Fourth column: Email
        'grade',                 # Fifth column: Grade
        'age',                   # Sixth column: Age
        'is_active',             # Seventh column: Active status
        'date_of_registration',  # Eighth column: Registration date
    ]
    
    # list_filter adds filter options on the right sidebar of admin
    # Users can filter students by these fields
    list_filter = [
        'grade',                 # Filter by grade (A, B, C, D, F)
        'is_active',             # Filter by active status
        'date_of_registration',  # Filter by registration date
        'age',                   # Filter by age
    ]
    
    # search_fields enables a search box to find students
    # Users can search by these fields
    # ^ means 'starts with' for faster searching
    search_fields = [
        '^first_name',           # Search starting with first name
        '^last_name',            # Search starting with last name
        'email',                 # Search by email (anywhere in the field)
        'roll_number',           # Search by roll number
        'phone_number',          # Search by phone number
    ]
    
    # fieldsets organizes fields in the student form/detail view
    # Groups related fields together for better organization
    fieldsets = (
        # First section: Personal Information
        ('Personal Information', {
            'fields': (
                'first_name',
                'last_name',
                'date_of_birth',
                'age',
            )
        }),
        # Second section: Contact Information
        ('Contact Information', {
            'fields': (
                'email',
                'phone_number',
                'address',
            )
        }),
        # Third section: Academic Information
        ('Academic Information', {
            'fields': (
                'roll_number',
                'grade',
            )
        }),
        # Fourth section: Status Information
        ('Status', {
            'fields': (
                'is_active',
                'date_of_registration',
                'updated_at',
            ),
            # classes adds CSS classes to the section
            # 'collapse' makes this section collapsible in admin
            'classes': ('collapse',),
        }),
    )
    
    # readonly_fields specifies fields that cannot be edited
    # These fields can only be viewed
    readonly_fields = [
        'date_of_registration',  # Auto-filled on creation
        'updated_at',            # Auto-updated on every save
    ]
    
    # ordering specifies the default order in the list view
    # '-date_of_registration' means sort by registration date, newest first
    ordering = ['-date_of_registration']
    
    # list_per_page sets how many records to show per page
    # Helps with performance for large datasets
    list_per_page = 20
    
    # date_hierarchy adds date-based navigation above the list
    # Allows drilling down by registration date
    date_hierarchy = 'date_of_registration'
