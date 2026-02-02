import json
from django import forms
from django.contrib.auth import get_user_model
from authentication.models import Employee, Employer, Township, Location
from django.core.exceptions import ValidationError
from django.forms import HiddenInput

User = get_user_model()

# 1. Form for common User data (Email & Profile Picture)
# class UserUpdateForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['email', 'profile_picture']

# 2. Form for Employee-specific data
# class EmployeeProfileForm(forms.ModelForm):
#     class Meta:
#         model = Employee
#         # Replace these with your actual Employee model fields
#         fields = ['profile_pic','employee_name','email','phone','state','Township','salary_expect','cv_file','experience','education','skills','social_media']

# 3. Form for Employer-specific data
class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = Employer
        exclude = (
            "user",
            "is_active",
            "created_at",
            "updated_at",
        )
        widgets = {
            "company_logo": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
            "company_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "industry": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "no_of_employee": forms.Select(
                attrs={"class": "form-control"}
            ),
            "founded_at": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "contact_email": forms.EmailInput(
                attrs={"class": "form-control"}
            ),
            "what_we_do": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "why_join_us": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "mission_vision": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
        }


# class EmployeeProfileForm(forms.ModelForm):
#     # We'll render JSON fields via JS and store JSON string into these hidden fields.
#     experience = forms.CharField(required=False, widget=HiddenInput())
#     education = forms.CharField(required=False, widget=HiddenInput())
#     skills = forms.CharField(required=False, widget=HiddenInput())
#     social_media = forms.CharField(required=False, widget=HiddenInput())
#
#     class Meta:
#         model = Employee
#         # Exclude fields we don't want the user to edit
#         exclude = ['is_active', 'user']
#         widgets = {
#             'employee_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#             'phone': forms.TextInput(attrs={'class': 'form-control'}),
#             "state": forms.Select(attrs={
#                 "class": "form-control",
#                 "id": "id_state"
#             }),
#                         "township": forms.Select(attrs={
#                 "class": "form-control",
#                 "id": "id_township"
#             }),
#             'salary_expect': forms.NumberInput(attrs={'class': 'form-control'}),
#             'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control'}),
#             'cv_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
#         }
#
#     def __init__(self, *args, **kwargs):
#         # Accept instance to prefill JSON fields as JSON strings
#         super().__init__(*args, **kwargs)
#         # 🔹 IMPORTANT: hide township until state selected
#         self.fields["township"].queryset = Township.objects.none()
#
#         if self.instance.pk and self.instance.state:
#             self.fields["township"].queryset = Township.objects.filter(
#                 state=self.instance.state
#             )
#         instance = kwargs.get('instance', None)
#         if instance:
#             # Convert python lists/dicts to JSON strings for the hidden inputs
#             self.initial.setdefault('experience', json.dumps(instance.experience or []))
#             self.initial.setdefault('education', json.dumps(instance.education or []))
#             self.initial.setdefault('skills', json.dumps(instance.skills or []))
#             self.initial.setdefault('social_media', json.dumps(instance.social_media or {}))
#
#
#
#     def clean_experience(self):
#         data = self.cleaned_data.get('experience', '')
#         if not data:
#             return []
#         try:
#             parsed = json.loads(data)
#             if not isinstance(parsed, list):
#                 raise ValidationError("Experience must be a JSON list.")
#             return parsed
#         except ValueError:
#             raise ValidationError("Invalid JSON for experience.")
#
#     def clean_education(self):
#         data = self.cleaned_data.get('education', '')
#         if not data:
#             return []
#         try:
#             parsed = json.loads(data)
#             if not isinstance(parsed, list):
#                 raise ValidationError("Education must be a JSON list.")
#             return parsed
#         except ValueError:
#             raise ValidationError("Invalid JSON for education.")
#
#     def clean_skills(self):
#         data = self.cleaned_data.get('skills', '')
#         if not data:
#             return []
#         try:
#             parsed = json.loads(data)
#             if not isinstance(parsed, list):
#                 raise ValidationError("Skills must be a JSON list.")
#             return parsed
#         except ValueError:
#             raise ValidationError("Invalid JSON for skills.")
#
#     def clean_social_media(self):
#         data = self.cleaned_data.get('social_media', '')
#         if not data:
#             return {}
#         try:
#             parsed = json.loads(data)
#             if not isinstance(parsed, dict):
#                 raise ValidationError("Social media must be a JSON object (key:value).")
#             return parsed
#         except ValueError:
#             raise ValidationError("Invalid JSON for social media.")

class EmployeeProfileForm(forms.ModelForm):
    # JSON Fields rendered via JS
    experience = forms.CharField(required=False, widget=HiddenInput())
    education = forms.CharField(required=False, widget=HiddenInput())
    skills = forms.CharField(required=False, widget=HiddenInput())
    social_media = forms.CharField(required=False, widget=HiddenInput())

    class Meta:
        model = Employee
        exclude = ['is_active', 'user']
        widgets = {
            'employee_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            "state": forms.Select(attrs={"class": "form-control", "id": "id_state"}),
            "township": forms.Select(attrs={"class": "form-control", "id": "id_township"}),
            'salary_expect': forms.NumberInput(attrs={'class': 'form-control'}),
            'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'cv_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 1. FIX: Handle Dependent Dropdown Validation
        # Start with an empty queryset
        self.fields["township"].queryset = Township.objects.none()

        # If the form was submitted (POST), use the submitted state to populate townships
        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['township'].queryset = Township.objects.filter(state_id=state_id)
            except (ValueError, TypeError):
                pass
                # If loading an existing record (GET), populate townships based on saved state
        elif self.instance.pk and self.instance.state:
            self.fields["township"].queryset = Township.objects.filter(state=self.instance.state)

        # 2. Populate JSON hidden fields with initial data
        if self.instance.pk:
            self.initial['experience'] = json.dumps(self.instance.experience or [])
            self.initial['education'] = json.dumps(self.instance.education or [])
            self.initial['skills'] = json.dumps(self.instance.skills or [])
            self.initial['social_media'] = json.dumps(self.instance.social_media or {})

        self.fields['township'].label_from_instance = lambda obj: f"{obj.name}"

    # 3. Clean Methods (Simplified to avoid repetition)
    def clean_json_field(self, field_name, expected_type):
        data = self.cleaned_data.get(field_name, '')
        if not data:
            return expected_type()  # Returns [] or {}
        try:
            parsed = json.loads(data)
            if not isinstance(parsed, expected_type):
                raise ValidationError(
                    f"{field_name.replace('_', ' ').capitalize()} must be a {expected_type.__name__}.")
            return parsed
        except ValueError:
            raise ValidationError(f"Invalid JSON format for {field_name}.")

    def clean_experience(self):
        return self.clean_json_field('experience', list)

    def clean_education(self):
        return self.clean_json_field('education', list)

    def clean_skills(self):
        return self.clean_json_field('skills', list)

    def clean_social_media(self):
        return self.clean_json_field('social_media', dict)

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        exclude = ("employer",)
        widgets = {
            "state": forms.Select(
                attrs={
                    "class": "form-control",
                    "id": "id_state",
                }
            ),
            "township": forms.Select(
                attrs={
                    "class": "form-control",
                    "id": "id_township",
                }
            ),
            "detail_address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "placeholder": "House No, Street Name, Ward, etc.",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 🔥 default: no township until state selected
        self.fields["township"].queryset = Township.objects.none()

        # 🔁 POST request
        if "state" in self.data:
            try:
                state_id = int(self.data.get("state"))
                self.fields["township"].queryset = Township.objects.filter(
                    state_id=state_id
                )
            except (ValueError, TypeError):
                pass

        # 🔁 EDIT mode
        elif self.instance.pk and self.instance.state:
            self.fields["township"].queryset = Township.objects.filter(
                state=self.instance.state
            )




