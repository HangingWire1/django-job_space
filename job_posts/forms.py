# apps/jobs/forms.py
from django import forms

from authentication.models import State, Township
from .models import JobPost

class JobPostForm(forms.ModelForm):
    # Manual fields for the Location model
    state = forms.ModelChoiceField(
        queryset=State.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    township = forms.ModelChoiceField(
        queryset=Township.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    detail_address = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Building, street, directions...'
        })
    )
    class Meta:
        model = JobPost
        # exclude employer because we set it in the view
        fields = [
            'title', 'salary', 'job_type',
            'category', 'description', 'requirements', 'contact_email',
            'slug'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job title'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 50000.00'}),
            'job_type': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Describe the job...'}),
            'requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Requirements, qualifications...'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'contact@example.com'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional: custom URL slug (leave blank to auto-generate)'}),
        }

    def clean_salary(self):
        salary = self.cleaned_data.get('salary')
        if salary is not None and salary < 0:
            raise forms.ValidationError("Salary must be a positive number.")
        return salary