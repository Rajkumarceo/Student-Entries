"""
Django views for the student_app.

Views are Python functions or classes that receive a request and return a response.
They contain the business logic for handling student data.
"""

from django.shortcuts import render, redirect, get_object_or_404
# render: renders a template with context
# redirect: redirects to another URL
# get_object_or_404: gets an object or returns 404 error if not found

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# Generic class-based views for common patterns

from django.contrib import messages
# messages: framework for displaying one-time notifications to users

from django.db.models import Q
# Q: allows complex database queries with OR, AND logic

from django.urls import reverse_lazy
# reverse_lazy: lazily evaluates URL reversal (used in class-based views)

from .models import Student
from .forms import StudentForm


# ==================== Function-Based Views ====================

def student_list(request):
    """
    Display a list of all students.
    
    This is a function-based view that handles GET requests to show all students.
    """
    # Fetch all student records from database
    students = Student.objects.all()
    
    # Get the search query from URL parameters (if any)
    search_query = request.GET.get('search', '')
    
    # If search query exists, filter students by name or email
    if search_query:
        # Q objects allow OR queries (| means OR, & means AND)
        # icontains: case-insensitive 'contains' search
        students = students.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(roll_number__icontains=search_query)
        )
    
    # Create context dictionary to pass to template
    context = {
        'students': students,  # List of student objects
        'search_query': search_query,  # Current search query
        'total_students': Student.objects.count(),  # Total student count
    }
    
    # render() loads the template and fills it with context data
    return render(request, 'student_app/student_list.html', context)


def student_detail(request, pk):
    """
    Display detailed information about a single student.
    
    Args:
        request: HTTP request object
        pk: primary key (ID) of the student to display
    """
    # Get the student object with given pk, or return 404 if not found
    student = get_object_or_404(Student, pk=pk)
    
    # Create context with the student object
    context = {
        'student': student,  # Single student object
    }
    
    # Render the detail template with student data
    return render(request, 'student_app/student_detail.html', context)


def student_create(request):
    """
    Handle creation of a new student record.
    
    GET request: Display form
    POST request: Process form submission and create student
    """
    # Check if request method is POST (form submission)
    if request.method == 'POST':
        # Create form instance with POST data
        form = StudentForm(request.POST)
        
        # Validate the form
        if form.is_valid():
            # Save the form (creates a new Student object in database)
            student = form.save()
            
            # Add success message to display to user
            messages.success(
                request,
                f'Student {student.first_name} {student.last_name} created successfully!'
            )
            
            # Redirect to the student's detail page
            return redirect('student_detail', pk=student.pk)
    else:
        # For GET requests, display an empty form
        form = StudentForm()
    
    # Create context with the form
    context = {
        'form': form,
        'title': 'Create New Student',
    }
    
    # Render the form template
    return render(request, 'student_app/student_form.html', context)


def student_update(request, pk):
    """
    Handle updating an existing student record.
    
    GET request: Display form with current data
    POST request: Process form submission and update student
    """
    # Get the student object to update
    student = get_object_or_404(Student, pk=pk)
    
    # Check if request method is POST (form submission)
    if request.method == 'POST':
        # Create form instance with POST data and existing student instance
        # instance=student pre-fills the form with current data
        form = StudentForm(request.POST, instance=student)
        
        # Validate the form
        if form.is_valid():
            # Save the changes to database
            student = form.save()
            
            # Add success message
            messages.success(
                request,
                f'Student {student.first_name} {student.last_name} updated successfully!'
            )
            
            # Redirect to the student's detail page
            return redirect('student_detail', pk=student.pk)
    else:
        # For GET requests, display form pre-filled with student data
        form = StudentForm(instance=student)
    
    # Create context with form and student
    context = {
        'form': form,
        'student': student,
        'title': f'Edit {student.first_name} {student.last_name}',
    }
    
    # Render the form template
    return render(request, 'student_app/student_form.html', context)


def student_delete(request, pk):
    """
    Handle deletion of a student record.
    
    GET request: Display confirmation page
    POST request: Actually delete the student
    """
    # Get the student object to delete
    student = get_object_or_404(Student, pk=pk)
    
    # Check if request method is POST (confirmed deletion)
    if request.method == 'POST':
        # Store student name before deletion
        student_name = f'{student.first_name} {student.last_name}'
        
        # Delete the student from database
        student.delete()
        
        # Add success message
        messages.success(
            request,
            f'Student {student_name} deleted successfully!'
        )
        
        # Redirect to student list
        return redirect('student_list')
    
    # Create context with student (for confirmation page)
    context = {
        'student': student,
    }
    
    # Render the confirmation template
    return render(request, 'student_app/student_confirm_delete.html', context)


# ==================== Class-Based Views (Alternative Approach) ====================
# These accomplish the same things as function-based views but with less code

class StudentListView(ListView):
    """
    Class-based view for listing all students.
    
    Automatically:
    - Fetches all objects from model
    - Paginates results
    - Renders default template
    """
    # model: specifies which model to query
    model = Student
    
    # template_name: custom template path (default: student_list.html)
    template_name = 'student_app/student_list.html'
    
    # context_object_name: variable name in template (default: object_list)
    context_object_name = 'students'
    
    # paginate_by: number of items per page
    paginate_by = 10


class StudentDetailView(DetailView):
    """
    Class-based view for displaying a single student's details.
    """
    model = Student
    template_name = 'student_app/student_detail.html'
    context_object_name = 'student'


class StudentCreateView(CreateView):
    """
    Class-based view for creating a new student.
    
    Handles both GET (display form) and POST (save data) automatically.
    """
    model = Student
    form_class = StudentForm
    template_name = 'student_app/student_form.html'
    
    # reverse_lazy: lazily evaluate the URL when needed
    # Used to redirect after successful creation
    success_url = reverse_lazy('student_list')
    
    def form_valid(self, form):
        """
        Called when form validation succeeds.
        Used to add messages or modify data before saving.
        """
        # Add success message
        messages.success(
            self.request,
            f'Student created successfully!'
        )
        
        # Call parent's form_valid to actually save the form
        return super().form_valid(form)


class StudentUpdateView(UpdateView):
    """
    Class-based view for updating an existing student.
    """
    model = Student
    form_class = StudentForm
    template_name = 'student_app/student_form.html'
    
    def get_success_url(self):
        """
        Determine the URL to redirect to after successful update.
        """
        # Redirect to the student's detail page
        return reverse_lazy('student_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        """
        Called when form validation succeeds.
        """
        messages.success(
            self.request,
            f'Student updated successfully!'
        )
        return super().form_valid(form)


class StudentDeleteView(DeleteView):
    """
    Class-based view for deleting a student.
    """
    model = Student
    template_name = 'student_app/student_confirm_delete.html'
    success_url = reverse_lazy('student_list')
    context_object_name = 'student'
    
    def delete(self, request, *args, **kwargs):
        """
        Called to delete the object.
        """
        # Add success message before deletion
        messages.success(
            request,
            f'Student deleted successfully!'
        )
        return super().delete(request, *args, **kwargs)
