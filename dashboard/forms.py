import uuid

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from authentication.models import Employee, Employer, State, Township
from job_posts.models import Category

User = get_user_model()

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class StateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = '__all__'

class TownshipForm(forms.ModelForm):
    class Meta:
        model = Township
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter township name'
            })
        }



class AddUserForm(UserCreationForm):
    name = forms.CharField(max_length=255, required=False, label="Name (employee or company name)")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'name', 'email', 'is_employer', 'is_employee',
            'is_active', 'is_staff', 'is_superuser',
            'groups', 'user_permissions'
        )

    def save(self, commit=True):
        # 1. Prepare the user object (commit=False)
        user = super().save(commit=False)

        # 2. Set the username BEFORE the first save to avoid IntegrityError
        if not user.username:
            if user.is_employee:
                user.username = f"employee_{uuid.uuid4().hex[:8]}"
            elif user.is_employer:
                user.username = f"employer_{uuid.uuid4().hex[:8]}"
            else:
                # Fallback if neither is selected
                user.username = f"user_{uuid.uuid4().hex[:8]}"

        if commit:
            user.save()  # This triggers your signal in signals.py!

            # 3. Handle Many-to-Many (Groups/Perms)
            # Use self.save_m2m(), NOT self.save()
            self.save_m2m()

            # 4. Update the profile name (since signal created the profile)
            name = self.cleaned_data.get('name')
            if name:
                if user.is_employee and hasattr(user, 'employee'):
                    user.employee.employee_name = name
                    user.employee.save()
                elif user.is_employer and hasattr(user, 'employer'):
                    user.employer.company_name = name
                    user.employer.save()

        return user

class EditUserForm(forms.ModelForm):
    name = forms.CharField(max_length=255, required=False, label="Name (employee or company name)")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'name', 'email', 'is_employer', 'is_employee',
            'is_active', 'is_staff', 'is_superuser',
            'groups', 'user_permissions'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Check if we are editing an existing user
        if self.instance and self.instance.pk:
            if self.instance.is_employee and hasattr(self.instance, 'employee'):
                self.fields['name'].initial = self.instance.employee.employee_name
            elif self.instance.is_employer and hasattr(self.instance, 'employer'):
                self.fields['name'].initial = self.instance.employer.company_name

    def save(self, commit=True):
        # 1. Prepare the user object (commit=False)
        user = super().save(commit=False)

        # 2. Set the username BEFORE the first save to avoid IntegrityError
        if not user.username:
            if user.is_employee:
                user.username = f"employee_{uuid.uuid4().hex[:8]}"
            elif user.is_employer:
                user.username = f"employer_{uuid.uuid4().hex[:8]}"
            else:
                # Fallback if neither is selected
                user.username = f"user_{uuid.uuid4().hex[:8]}"

        if commit:
            user.save()  # This triggers your signal in signals.py!

            # 3. Handle Many-to-Many (Groups/Perms)
            # Use self.save_m2m(), NOT self.save()
            self.save_m2m()

            # 4. Update the profile name (since signal created the profile)
            name = self.cleaned_data.get('name')
            if name:
                if user.is_employee and hasattr(user, 'employee'):
                    user.employee.employee_name = name
                    user.employee.save()
                elif user.is_employer and hasattr(user, 'employer'):
                    user.employer.company_name = name
                    user.employer.save()

        return user

# class EditUserForm(forms.ModelForm):
#     # Manually add the profile fields
#     name = forms.CharField(max_length=255, required=False, label="Name (employee or company name)")
#
#     class Meta:
#         model = User
#         fields = (
#             'name', 'email', 'is_employer', 'is_employee',
#             'is_active', 'is_staff', 'is_superuser',
#             'groups', 'user_permissions'
#         )
#
#     def save(self, commit=True):
#         # 1. Save the User first
#         user = super().save(commit=False)
#
#         if commit:
#             user.save()
#             # 2. Get the name from the form
#             name = self.cleaned_data.get('name')
#
#             # 3. Create the related profile based on the toggle
#             if user.is_employee:
#                 Employee.objects.get_or_create(user=user, employee_name=name)
#             elif user.is_employer:
#                 Employer.objects.get_or_create(user=user, employer_name=name)
#
#             # Save many-to-many fields (groups/permissions)
#             self.save_m2m()
#         return user
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         # Check if we are editing an existing user (instance)
#         if self.instance and self.instance.pk:
#             # Look for the name in the related models
#             if self.instance.is_employee and hasattr(self.instance, 'employee'):
#                 self.fields['name'].initial = self.instance.employee.employee_name
#             elif self.instance.is_employer and hasattr(self.instance, 'employer'):
#                 self.fields['name'].initial = self.instance.employer.company_name

