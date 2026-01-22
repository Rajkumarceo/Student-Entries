"""
Django forms for the student_app.

Forms handle user input, validation, and conversion to model instances.
They're used for creating and updating student records through web pages.
"""

from django import forms
# forms module provides form field types and the ModelForm base class

from .models import Student
# Import the Student model


class StudentForm(forms.ModelForm):
    """
    StudentForm is a ModelForm that creates a form from the Student model.
    
    ModelForms automatically generate form fields based on model fields.
    This reduces code duplication and keeps forms synchronized with models.
    """
    
    class Meta:
        # Meta class provides options for the ModelForm
        
        # model specifies which model this form is based on
        model = Student
        
        # fields specifies which model fields to include in the form
        # '__all__' means include all fields
        # You can also use a list: ['first_name', 'last_name', 'email', ...]
        fields = '__all__'
        
        # exclude would remove specific fields (if needed)
        # exclude = ['date_of_registration', 'updated_at']
    
    # Customize form fields with additional properties
    def __init__(self, *args, **kwargs):
        """
        __init__ customizes the form after it's created.
        
        *args: positional arguments from parent class
        **kwargs: keyword arguments from parent class
        """
        # Call the parent class's __init__ method
        super().__init__(*args, **kwargs)
        
        # Customize each field's appearance and behavior
        # Add Bootstrap CSS class for styling
        
        # first_name field customization
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',  # Bootstrap class for styling
            'placeholder': 'Enter first name',  # Hint text in input
        })
        
        # last_name field customization
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter last name',
        })
        
        # email field customization
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter email address',
            'type': 'email',  # HTML5 email type
        })
        
        # roll_number field customization
        self.fields['roll_number'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter roll number',
            'type': 'number',
        })
        
        # grade field customization
        self.fields['grade'].widget.attrs.update({
            'class': 'form-control',  # Select dropdown styling
        })
        
        # age field customization
        self.fields['age'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter age',
            'type': 'number',
            'min': '1',  # HTML5 validation: minimum value
            'max': '100',  # HTML5 validation: maximum value
        })
        
        # date_of_birth field customization
        self.fields['date_of_birth'].widget.attrs.update({
            'class': 'form-control',
            'type': 'date',  # HTML5 date picker
        })
        
        # address field customization
        self.fields['address'].widget.attrs.update({
            'class': 'form-control',
            'rows': '4',  # TextArea with 4 rows
            'placeholder': 'Enter address',
        })
        
        # phone_number field customization
        self.fields['phone_number'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter phone number',
            'type': 'tel',  # HTML5 telephone type
        })
        
        # is_active field customization
        self.fields['is_active'].widget.attrs.update({
            'class': 'form-check-input',  # Bootstrap checkbox styling
        })
    
    # Custom validation method for the form
    def clean(self):
        """
        clean() is called when form.is_valid() is executed.
        
        It performs custom validation on multiple fields.
        Raises ValidationError if validation fails.
        """
        # Call parent's clean method first
        cleaned_data = super().clean()
        
        # Get the cleaned (validated) data from form
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        age = cleaned_data.get('age')
        
        # Validate that first and last names are not the same
        if first_name and last_name and first_name.lower() == last_name.lower():
            # Raise an error that applies to the whole form
            raise forms.ValidationError(
                "First name and last name cannot be the same."
            )
        
        # Validate that age is reasonable
        if age and (age < 5 or age > 100):
            # Add error to specific field
            self.add_error('age', 'Age must be between 5 and 100.')
        
        # Always return cleaned_data
        return cleaned_data
