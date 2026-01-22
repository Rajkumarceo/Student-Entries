"""
ASGI config for student_project project.

ASGI (Asynchronous Server Gateway Interface) is used for async web servers.
This is the entry point for ASGI servers like Uvicorn, Daphne, etc.
"""

import os

from django.core.asgi import get_asgi_application

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_project.settings')

# Get the ASGI application
application = get_asgi_application()
