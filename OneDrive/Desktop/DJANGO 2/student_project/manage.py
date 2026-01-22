#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.
This file is created by django-admin startproject and allows you to:
- Run the development server
- Create migrations
- Run migrations
- Create superuser
- And many more Django management commands
"""
import os
import sys


def main():
    """
    Run administrative tasks.
    This is the entry point for Django management commands.
    """
    # Set the Django settings module to use the configuration from settings.py
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_project.settings')
    try:
        # Import the execute_from_command_line function from Django
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # If Django is not installed, raise an error with helpful message
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Execute the command line arguments passed to this script
    execute_from_command_line(sys.argv)


# Standard Python pattern to ensure code only runs when script is executed directly
if __name__ == '__main__':
    main()
