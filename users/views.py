from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .forms import RegisterForm, LoginForm, ProfileEditForm, AdminUserEditForm
from .models import CustomUser


# Handles new user registration. Redirects to home if already logged in.
# On successful form submission, logs the user in immediately.
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}! Your account has been created.')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


# Authenticates the user and starts a session. Supports ?next= redirect after login.
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect(request.GET.get('next', 'home'))
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


# Clears the session and redirects to the login page.
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


# Shows a user's profile. If a username is provided in the URL, shows that user's
# profile; otherwise defaults to the currently logged-in user.
@login_required
def profile_view(request, username=None):
    if username:
        profile_user = get_object_or_404(CustomUser, username=username)
    else:
        profile_user = request.user
    return render(request, 'users/profile.html', {'profile_user': profile_user})


# Lets the logged-in user update their own profile fields and profile picture.
@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'users/profile_edit.html', {'form': form})


# Admin-only view that lists all registered users.
@login_required
def admin_user_list(request):
    if not request.user.is_admin():
        return HttpResponseForbidden("Access denied.")
    users = CustomUser.objects.all().order_by('username')
    return render(request, 'users/admin_user_list.html', {'users': users})


# Admin-only view for changing a user's role or active status.
@login_required
def admin_user_edit(request, pk):
    if not request.user.is_admin():
        return HttpResponseForbidden("Access denied.")
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = AdminUserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f"User '{user.username}' updated successfully.")
            return redirect('admin_user_list')
    else:
        form = AdminUserEditForm(instance=user)
    return render(request, 'users/admin_user_edit.html', {'form': form, 'edited_user': user})


# Admin-only view for deleting a user. Prevents admins from deleting their own account.
@login_required
def admin_user_delete(request, pk):
    if not request.user.is_admin():
        return HttpResponseForbidden("Access denied.")
    user = get_object_or_404(CustomUser, pk=pk)
    if user == request.user:
        messages.error(request, "You cannot delete yourself.")
        return redirect('admin_user_list')
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f"User '{username}' deleted.")
        return redirect('admin_user_list')
    return render(request, 'users/admin_user_delete.html', {'edited_user': user})
