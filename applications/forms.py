from django import forms
from authentication.models import Employee  # Make sure to import your Employee model

class EmployeeApplicationForm(forms.ModelForm):
    # --- ADD THE NEW FIELDS HERE ---
    salary_expect = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 50000.00'}),
        required=False,
        help_text="Optional: What is your expected salary for this role?"
    )

    cover_letter = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'class': 'form-control', 'placeholder': 'Write a brief message to the employer...'}),
        required=False,
        help_text="Optional: A personal note to the hiring manager."
    )

    class Meta:
        model = Employee
        fields = ['employee_name', 'email', 'phone', 'cv_file']
        # ... widgets ...

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # --- Pre-fill the salary field if the employee has a default value ---
        # This makes it easier for the user, who can override it if they want.
        if self.instance and self.instance.salary_expect:
            self.fields['salary_expect'].initial = self.instance.salary_expect

        # --- Set which fields are required for submission ---
        self.fields['employee_name'].required = True
        self.fields['email'].required = True
        self.fields['cv_file'].required = True
        self.fields['phone'].required = False
