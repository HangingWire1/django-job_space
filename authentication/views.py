from django.contrib import messages, auth
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from authentication.forms import EmployeeRegistrationForm, EmployeeLoginForm


def user_registration(request):
    current_active_page = request.session.get('active_page', 'employee')
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST,active_page=current_active_page)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect('home')
    else:
        form = EmployeeRegistrationForm(active_page=current_active_page)

    return render(request, 'authentication/User_registration.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = EmployeeLoginForm(request, data=request.POST)
        if form.is_valid():
            # No need to get email or password manually!
            # form.get_user() returns the authenticated user object
            user = form.get_user()

            # Now we just log them in
            login(request, user)
            return redirect('home')
    else:
        form = EmployeeLoginForm()

    return render(request, 'authentication/User_login.html', {'form': form})