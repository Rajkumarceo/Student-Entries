"""
Django app configuration for student_app.

Apps are Django's way of organizing functionality into separate modules.
The AppConfig class configures the app's metadata.
"""

from django.apps import AppConfig
# AppConfig: base class for app configuration


class StudentAppConfig(AppConfig):
    """
    Configuration class for the student_app application.
    """
    # default_auto_field: specifies the field type for auto-generated primary keys
    # BigAutoField: supports larger numbers (up to 9,223,372,036,854,775,807)
    default_auto_field = 'django.db.models.BigAutoField'
    
    # name: the name of the application as a Python module
    # Must match the app's folder name
    name = 'student_app'
    
    # verbose_name: human-readable name for the app
    # Used in Django admin and other places
    verbose_name = 'Student Management'
