"""
URL Configuration for student_project.

This file defines the URL routes for the entire project.
It maps URL patterns to view functions that handle requests.

For example:
    http://localhost:8000/ -> home view
    http://localhost:8000/admin/ -> Django admin
    http://localhost:8000/student/ -> student app URLs
"""

from django.contrib import admin
from django.urls import path, include
# include() is used to reference URL patterns from other apps

urlpatterns = [
    # Django admin panel - built-in admin interface
    # Access at: http://localhost:8000/admin/
    path('admin/', admin.site.urls),
    
    # Include all URLs from the student_app
    # The 'student_app.urls' module contains all student-related URL patterns
    # The empty string '' means these URLs are at the root level
    path('', include('student_app.urls')),
]
