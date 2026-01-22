"""
URL Configuration for the student_app.

This file maps URL patterns to view functions/classes.
It defines the routes for student CRUD operations.
"""

from django.urls import path
# path(): maps a URL pattern to a view

from . import views
# Import all views from this app


# URL patterns list
urlpatterns = [
    # Student List View
    # URL: http://localhost:8000/
    # Function: Display all students
    path(
        '',  # Empty string means root URL
        views.student_list,  # View function to handle this URL
        name='student_list'  # Name used in reverse() and templates
    ),
    
    # Student Detail View
    # URL: http://localhost:8000/student/1/
    # <int:pk> is a URL parameter that captures an integer (student ID)
    path(
        'student/<int:pk>/',
        views.student_detail,
        name='student_detail'
    ),
    
    # Student Create View
    # URL: http://localhost:8000/create/
    # Function: Display form and handle new student creation
    path(
        'create/',
        views.student_create,
        name='student_create'
    ),
    
    # Student Update View
    # URL: http://localhost:8000/student/1/edit/
    # <int:pk> captures the student ID to edit
    path(
        'student/<int:pk>/edit/',
        views.student_update,
        name='student_update'
    ),
    
    # Student Delete View
    # URL: http://localhost:8000/student/1/delete/
    # <int:pk> captures the student ID to delete
    path(
        'student/<int:pk>/delete/',
        views.student_delete,
        name='student_delete'
    ),
]


# Alternative: Using Class-Based Views (CBV)
# Uncomment below to use CBV instead of function-based views
"""
urlpatterns = [
    path('', views.StudentListView.as_view(), name='student_list'),
    path('student/<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('create/', views.StudentCreateView.as_view(), name='student_create'),
    path('student/<int:pk>/edit/', views.StudentUpdateView.as_view(), name='student_update'),
    path('student/<int:pk>/delete/', views.StudentDeleteView.as_view(), name='student_delete'),
]
"""
