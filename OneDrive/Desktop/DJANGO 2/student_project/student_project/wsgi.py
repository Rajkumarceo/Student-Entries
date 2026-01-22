"""
WSGI config for student_project project.

WSGI (Web Server Gateway Interface) is the standard for Python web applications.
This file is used by production servers like Gunicorn, uWSGI, etc.
It's the entry point that production web servers call to run the Django application.
"""

import os

from django.core.wsgi import get_wsgi_application

# Set the Django settings module to use for this application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_project.settings')

# Create the WSGI application object
application = get_wsgi_application()
