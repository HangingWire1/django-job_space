from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory, modelformset_factory
from django.shortcuts import render

from dashboard.forms import CategoryForm, AddUserForm, EditUserForm, StateForm, TownshipForm
from job_posts.forms import JobPostForm
from job_posts.models import JobPost, Category
from authentication.models import User, Location, State, Township
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

@login_required(login_url='login')
def dashboard(request):
    # Count users based on their type
    employee_count = User.objects.filter(is_employee=True).count()
    employer_count = User.objects.filter(is_employer=True).count()

    # Count all job posts
    post_count = JobPost.objects.all().count()

    context = {
        'employee_count': employee_count,
        'employer_count': employer_count,
        'post_count': post_count,
    }
    return render(request, 'dashboard/dashboard.html', context)

#categories
def categories(request):
    cats = Category.objects.all()
    context = {'cats': cats}
    return render(request,'dashboard/category/categories.html', context)

def add_category(request):
    # Create a FormSet for Category. extra=1 provides one empty row by default.
    CategoryFormSet = modelformset_factory(Category, form=CategoryForm, extra=1)

    if request.method == "POST":
        formset = CategoryFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('categories')
    else:
        # Prevent existing categories from appearing in the "Add" view
        formset = CategoryFormSet(queryset=Category.objects.none())

    context = {
        'formset': formset,
    }
    return render(request, 'dashboard/category/add_category.html', context)

def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            print('form is valid')
            form.save()
            return redirect('categories')
        else:
            print('form is invalid')
            print('form.errors')
    form = CategoryForm(instance=category)
    context = {
        'form': form,
        'category': category,

    }
    return render(request,'dashboard/category/edit_category.html',context)

def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('categories')

#location/states
def states(request):
    states = State.objects.all()
    context = {'states': states}
    return render(request,'dashboard/states/states.html', context)

def add_state(request):
    # Create the FormSet class
    # extra=1 starts with one blank row
    StateFormSet = modelformset_factory(State, form=StateForm, extra=1)

    if request.method == "POST":
        # Bind the POST data
        formset = StateFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('states')
    else:
        # queryset=State.objects.none() ensures existing states don't show up
        formset = StateFormSet(queryset=State.objects.none())

    context = {
        'formset': formset,
    }
    return render(request, 'dashboard/states/add_state.html', context)

def edit_state(request, pk):
    state = get_object_or_404(State, pk=pk)
    if request.method == "POST":
        form = StateForm(request.POST, instance=state)
        if form.is_valid():
            print('form is valid')
            form.save()
            return redirect('states')
        else:
            print('form is invalid')
            print('form.errors')
    form = StateForm(instance=state)
    context = {
        'form': form,
        'state': state,

    }
    return render(request,'dashboard/states/edit_state.html',context)

def delete_state(request, pk):
    state = get_object_or_404(State, pk=pk)
    state.delete()
    return redirect('states')

#location/townships
def townships(request, state_id):
    townships = Township.objects.filter(state_id=state_id)
    state = get_object_or_404(State, pk=state_id)
    context = {'townships': townships, 'state': state}
    return render(request,'dashboard/townships/townships.html', context)

def add_township(request, state_id):
    state_obj = get_object_or_404(State, id=state_id)

    TownshipFormSet = inlineformset_factory(
        State,
        Township,
        form=TownshipForm,
        extra=1, # Number of empty rows to start with
        can_delete=True
    )

    if request.method == "POST":
        formset = TownshipFormSet(request.POST, instance=state_obj)
        if formset.is_valid():
            formset.save()
            return redirect('townships', state_id=state_obj.pk)
    else:
        # THE TRICK: Set the queryset to none()
        # This prevents existing townships from loading into the form
        formset = TownshipFormSet(
            instance=state_obj,
            queryset=Township.objects.none()
        )

    return render(request, 'dashboard/townships/add_township.html', {
        'formset': formset,
        'state': state_obj
    })

def edit_township(request, state_id, pk):
    township = get_object_or_404(Township, pk=pk)
    state = get_object_or_404(State, pk=state_id)
    if request.method == "POST":
        form = TownshipForm(request.POST, instance=township)
        if form.is_valid():
            print('form is valid')
            form.save()
            return redirect('townships', state_id=state_id)
        else:
            print('form is invalid')
            print('form.errors')
    form = TownshipForm(instance=township)
    context = {
        'form': form,
        'township': township,
        'state': state,

    }
    return render(request,'dashboard/townships/edit_township.html',context)

def delete_township(request, state_id, pk):
    # 1. Fetch the township or 404
    township = get_object_or_404(Township, pk=pk, state_id=state_id)
    # township_name = township.name  # Capture name for the message
    township.delete()

    # Optional: Add a success message
    # messages.success(request, f"Township '{township_name}' deleted successfully.")

    # 2. Redirect back to the township list for this specific state
    return redirect('townships', state_id=state_id)

#posts
def posts(request):
    # Use select_related to avoid N+1 queries for employer and category
    posts = JobPost.objects.all().select_related('employer', 'category')

    # Get filter values from the URL
    search_query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    archive_filter = request.GET.get('archive', '')

    # Apply Search by Title
    if search_query:
        posts = posts.filter(title__icontains=search_query)

    # Apply Status Filter
    if status_filter:
        posts = posts.filter(status=status_filter)

    # Apply Archive Filter
    if archive_filter == 'true':
        posts = posts.filter(is_archived=True)
    elif archive_filter == 'false':
        posts = posts.filter(is_archived=False)

    context = {
        'posts': posts,
        'search_query': search_query,
        'status_filter': status_filter,
        'archive_filter': archive_filter,
    }
    return render(request, 'dashboard/post/posts.html', context)

def add_post(request):
    # Find employer profile for the logged in user.
    employer = getattr(request.user, 'employer', None)

    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            loc, created = Location.objects.get_or_create(
                state=form.cleaned_data['state'],
                township=form.cleaned_data['township'],
                detail_address=form.cleaned_data['detail_address']
            )
            job.location = loc
            job.employer = employer
            job.save()
            print(job.location.state, job.location.township,job.location.detail_address),
            messages.success(request, "Job added successfully.")
            # redirect to job detail or job list — change 'job_detail' to your route name
            # return redirect('job_detail', slug=job.slug)
            return redirect('posts')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = JobPostForm()

    context = {
        'form': form,
    }
    return render(request, 'dashboard/post/add_post.html',context)

def edit_post(request, pk):
    # employer = request.user.employer
    job = get_object_or_404(JobPost, pk=pk)

    location = job.location  # existing location

    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job)

        if form.is_valid():
            job = form.save(commit=False)

            # Update Location manually
            state = form.cleaned_data['state']
            township = form.cleaned_data['township']
            detail_address = form.cleaned_data['detail_address']

            location.state = state
            location.township = township
            location.detail_address = detail_address
            location.save()

            job.location = location
            job.save()

            messages.success(request, "Job updated successfully.")
            return redirect('posts')
    else:
        # Pre-fill manual fields
        form = JobPostForm(instance=job, initial={
            'state': location.state,
            'township': location.township,
            'detail_address': location.detail_address,
        })

    return render(request, 'dashboard/post/edit_post.html', {'form': form, 'job': job})

def delete_post(request, pk):
    post = get_object_or_404(JobPost, pk=pk)
    post.delete()
    return redirect('posts')

#users
def users(request):
    users = User.objects.all().prefetch_related('groups', 'employee', 'employer')

    # Get parameters from the URL
    search_query = request.GET.get('q', '')
    user_type = request.GET.get('user_type', '')

    # Filter by User Type (Employer/Employee)
    if user_type == 'employee':
        users = users.filter(is_employee=True)
    elif user_type == 'employer':
        users = users.filter(is_employer=True)

    # Filter by Search Query (Email or Profile Names)
    if search_query:
        users = users.filter(
            Q(email__icontains=search_query) |
            Q(employee__employee_name__icontains=search_query) |
            Q(employer__company_name__icontains=search_query)
        ).distinct()  # distinct() prevents duplicates if one user matches multiple conditions

    context = {
        'users': users,
        'search_query': search_query,
        'user_type': user_type,
    }
    return render(request, 'dashboard/user/users.html', context)

def add_user(request):
    if request.method == "POST":
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users')
        else:
            print(form.errors)
    form = AddUserForm()
    context = {
        'form': form,
    }
    return render(request,'dashboard/user/add_user.html',context)

def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            print("form is valid and saved")
            return redirect('users')
        print("form is invalid!!!")
    form = EditUserForm(instance=user)
    context = {
        'form': form,
        'user': user,
    }
    return render(request,'dashboard/user/edit_user.html',context)

def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect('users')
