"""
Django settings for student_project project.

This file contains all the configuration settings for the Django project.
Key areas include:
- Database configuration
- Installed apps
- Templates and static files
- Security settings
- And many more configurations
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR is the root directory of the entire project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY is used for cryptographic signing (sessions, CSRF tokens, etc.)
# In production, this should be kept in environment variables, NOT in source code
SECRET_KEY = 'django-insecure-your-secret-key-change-this-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True enables detailed error pages and serves static files automatically
# Set to False in production for security
DEBUG = True

# ALLOWED_HOSTS specifies which domain names this Django site can serve
# '*' allows all hosts (only for development!)
# In production, list only your actual domain names like ['example.com', 'www.example.com']
ALLOWED_HOSTS = ['*']


# Application definition
# INSTALLED_APPS lists all the apps that are part of this project
INSTALLED_APPS = [
    # Django's default apps that provide core functionality
    'django.contrib.admin',      # Admin interface
    'django.contrib.auth',       # Authentication system
    'django.contrib.contenttypes',  # Content type framework
    'django.contrib.sessions',   # Session management
    'django.contrib.messages',   # Messaging framework for notifications
    'django.contrib.staticfiles',  # Static files management
    
    # Our custom app for student management
    'student_app',
]

# MIDDLEWARE is a list of hooks/processes that run on every request and response
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Adds security headers
    'django.contrib.sessions.middleware.SessionMiddleware',  # Session handling
    'django.middleware.common.CommonMiddleware',  # Common utilities (CSRF protection, etc.)
    'django.middleware.csrf.CsrfViewMiddleware',  # Cross-Site Request Forgery protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # User authentication
    'django.contrib.messages.middleware.MessageMiddleware',  # Message framework
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking protection
]

# ROOT_URLCONF specifies the Python module where URL patterns are defined
ROOT_URLCONF = 'student_project.urls'

# TEMPLATES configuration
# This tells Django where to find template files and how to render them
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # DIR specifies additional directories to search for templates
        # BASE_DIR / 'templates' means a 'templates' folder in the project root
        'DIRS': [BASE_DIR / 'templates'],
        # APP_DIRS = True makes Django search for templates inside each app's 'templates' folder
        'APP_DIRS': True,
        # OPTIONS contains template processing options
        'OPTIONS': {
            # context_processors are functions that add variables to every template
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI_APPLICATION specifies the WSGI application to use when serving the project
WSGI_APPLICATION = 'student_project.wsgi.application'


# Database configuration
# This project uses SQLite (default for development)
# For production, use PostgreSQL, MySQL, or other databases
DATABASES = {
    # 'default' is the database used unless otherwise specified
    'default': {
        # SQLite is a file-based database, perfect for development
        'ENGINE': 'django.db.backends.sqlite3',
        # This creates a 'db.sqlite3' file in the BASE_DIR
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# PASSWORD_VALIDATORS check password strength when users create/change passwords
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# LANGUAGE_CODE and TIME_ZONE set the default locale and timezone
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

# USE_I18N enables Django's translation system
USE_I18N = True

# USE_TZ enables timezone support
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# STATIC_URL is the URL prefix for serving static files
STATIC_URL = '/static/'

# STATIC_ROOT is where collectstatic collects static files for production
STATIC_ROOT = BASE_DIR / 'staticfiles'

# STATICFILES_DIRS tells Django where to find additional static files
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files (User uploads)
# MEDIA_URL is the URL prefix for user-uploaded files
MEDIA_URL = '/media/'

# MEDIA_ROOT is the directory where uploaded files are stored
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# This specifies the default field type for primary keys
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
