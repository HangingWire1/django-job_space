from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST


def home(request):
    # If 'active_page' isn't in the session yet, set it to employee
    if 'active_page' not in request.session:
        request.session['active_page'] = 'employee'
        request.session.set_expiry(None)
    return render(request, 'home.html')

@require_POST
def active_page(request):
        # 1. Get current role
        current_role = request.session.get('active_page', 'employee')
        # print("current_role==", current_role)
        # 2. Toggle role
        new_role = 'employer' if current_role == 'employee' else 'employee'
        request.session['active_page'] = new_role
        # print("new_role==", request.session.get('active_page', 'employee'))

        # 3. Redirect back to where they came from
        return redirect(request.META.get('HTTP_REFERER', '/'))