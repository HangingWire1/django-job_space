
import uuid
from calendar import error

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.messages.storage import session

from authentication.models import User
from job_space_main.views import active_page


class EmployeeRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email",)

    def __init__(self, *args, **kwargs):
        # We "pop" the value out so the UserCreationForm doesn't get confused
        self.role_value = kwargs.pop('active_page', 'employee')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)
        # Use the value we captured in __init__
        if self.role_value == 'employee':
            user.is_employee = True
            # Generates something like employee_a1b2c3d4
            user.username = f"employee_{uuid.uuid4().hex[:8]}"
        elif self.role_value =='employer':
            user.is_employer = True
            # Generates something like employer_a1b2c3d4
            user.username = f"employer_{uuid.uuid4().hex[:8]}"
        else:
            #throw error
            print("active page==",self.role_value)
            raise forms.ValidationError("Invalid session role. Please restart registration.")

        if commit:
            user.save()
        return user

class EmployeeLoginForm(AuthenticationForm):
    # simply override the 'username' field to look like an email field
    username = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email Address'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))

    # email = forms.EmailField(required=True)
    #
    # class Meta(AuthenticationForm.Meta):
    #     model = User
    #     fields = ("email",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Change the label from "Username" to "Email"
        self.fields['username'].label = "Email"