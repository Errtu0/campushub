from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Club
from .forms import ClubForm


# Returns all approved clubs for the public listing page.
def club_list_view(request):
    clubs = Club.objects.filter(status='approved')
    return render(request, 'clubs/club_list.html', {'clubs': clubs})


# Shows the detail page for a single club. Unapproved clubs are only visible
# to the club's own manager and admins.
def club_detail_view(request, pk):
    club = get_object_or_404(Club, pk=pk)
    if not club.is_approved() and not (
        request.user.is_authenticated and (
            request.user.is_admin() or request.user == club.manager
        )
    ):
        return HttpResponseForbidden("This club is not yet approved.")

    is_member = request.user.is_authenticated and request.user in club.members.all()
    events = club.events.all().order_by('date')
    return render(request, 'clubs/club_detail.html', {
        'club': club,
        'is_member': is_member,
        'events': events,
    })


# Handles club creation. New clubs are saved with 'pending' status and
# must be approved by an admin before appearing publicly.
@login_required
def club_create_view(request):
    if not (request.user.is_club_manager() or request.user.is_admin()):
        messages.error(request, "Only club managers can create clubs.")
        return redirect('club_list')
    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES)
        if form.is_valid():
            club = form.save(commit=False)
            club.manager = request.user
            club.status = 'pending'
            club.save()
            messages.success(request, f'Club "{club.name}" created and submitted for approval.')
            return redirect('club_detail', pk=club.pk)
    else:
        form = ClubForm()
    return render(request, 'clubs/club_form.html', {'form': form, 'action': 'Create'})


# Allows the club's manager or an admin to edit club details and logo.
@login_required
def club_edit_view(request, pk):
    club = get_object_or_404(Club, pk=pk)
    if not (request.user.is_admin() or request.user == club.manager):
        return HttpResponseForbidden("You can only edit your own clubs.")
    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES, instance=club)
        if form.is_valid():
            form.save()
            messages.success(request, f'Club "{club.name}" updated.')
            return redirect('club_detail', pk=club.pk)
    else:
        form = ClubForm(instance=club)
    return render(request, 'clubs/club_form.html', {'form': form, 'action': 'Edit', 'club': club})


# Adds the current user to the club's member list.
# Only works for approved clubs; silently rejects if already a member.
@login_required
def club_join_view(request, pk):
    club = get_object_or_404(Club, pk=pk, status='approved')
    if request.method == 'POST':
        if request.user in club.members.all():
            messages.info(request, "You are already a member of this club.")
        else:
            club.members.add(request.user)
            messages.success(request, f'You have joined "{club.name}"!')
    return redirect('club_detail', pk=pk)


# Removes the current user from the club's member list.
@login_required
def club_leave_view(request, pk):
    club = get_object_or_404(Club, pk=pk)
    if request.method == 'POST':
        if request.user not in club.members.all():
            messages.info(request, "You are not a member of this club.")
        else:
            club.members.remove(request.user)
            messages.success(request, f'You have left "{club.name}".')
    return redirect('club_detail', pk=pk)


# Admin-only page that lists all pending clubs alongside all clubs.
@login_required
def admin_club_approval(request):
    if not request.user.is_admin():
        return HttpResponseForbidden("Access denied.")
    pending_clubs = Club.objects.filter(status='pending')
    all_clubs = Club.objects.all().order_by('-created_at')
    return render(request, 'clubs/admin_approval.html', {
        'pending_clubs': pending_clubs,
        'all_clubs': all_clubs,
    })


# Processes an approve or reject action for a specific club.
# Expects a POST with an 'action' field set to either 'approve' or 'reject'.
@login_required
def admin_club_approve(request, pk):
    if not request.user.is_admin():
        return HttpResponseForbidden("Access denied.")
    club = get_object_or_404(Club, pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            club.status = 'approved'
            club.save()
            messages.success(request, f'Club "{club.name}" approved.')
        elif action == 'reject':
            club.status = 'rejected'
            club.save()
            messages.warning(request, f'Club "{club.name}" rejected.')
    return redirect('admin_club_approval')


# Admin-only view for permanently deleting a club and all its related data.
@login_required
def admin_club_delete(request, pk):
    if not request.user.is_admin():
        return HttpResponseForbidden("Access denied.")
    club = get_object_or_404(Club, pk=pk)
    if request.method == 'POST':
        name = club.name
        club.delete()
        messages.success(request, f'Club "{name}" deleted.')
        return redirect('admin_club_approval')
    return render(request, 'clubs/club_delete_confirm.html', {'club': club})


# Dashboard for managers and admins. Admins see all clubs;
# managers only see the clubs they own.
@login_required
def manager_dashboard(request):
    if not (request.user.is_club_manager() or request.user.is_admin()):
        return HttpResponseForbidden("Access denied.")
    if request.user.is_admin():
        clubs = Club.objects.all()
    else:
        clubs = Club.objects.filter(manager=request.user)
    return render(request, 'clubs/manager_dashboard.html', {'clubs': clubs})
