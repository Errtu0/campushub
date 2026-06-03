from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from .models import Event, EventRegistration
from .forms import EventForm


# Lists all events belonging to approved clubs. Supports title search via ?q=
# and paginates results at 9 per page.
def event_list_view(request):
    events = Event.objects.filter(club__status='approved').select_related('club')
    query = request.GET.get('q')
    if query:
        events = events.filter(title__icontains=query)
    paginator = Paginator(events, 9)
    page = request.GET.get('page')
    events = paginator.get_page(page)
    return render(request, 'events/event_list.html', {'events': events, 'query': query})


# Shows the detail page for a single event. Also checks whether the current
# user is already registered so the template can show the right button.
def event_detail_view(request, pk):
    event = get_object_or_404(Event, pk=pk)
    is_registered = False
    if request.user.is_authenticated:
        is_registered = EventRegistration.objects.filter(event=event, user=request.user).exists()
    participants = event.registrations.select_related('user').all()
    return render(request, 'events/event_detail.html', {
        'event': event,
        'is_registered': is_registered,
        'participants': participants,
    })


# Handles event creation. Only club managers and admins can access this.
# Managers are restricted to creating events only for their own clubs.
@login_required
def event_create_view(request):
    if not (request.user.is_club_manager() or request.user.is_admin()):
        messages.error(request, "Only club managers can create events.")
        return redirect('event_list')
    if request.method == 'POST':
        form = EventForm(request.POST, user=request.user)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            if request.user.is_club_manager() and event.club.manager != request.user:
                messages.error(request, "You can only create events for your own clubs.")
                return redirect('event_create')
            event.save()
            messages.success(request, f'Event "{event.title}" created successfully.')
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm(user=request.user)
    return render(request, 'events/event_form.html', {'form': form, 'action': 'Create'})


# Allows the event creator or an admin to edit event details.
@login_required
def event_edit_view(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if not (request.user.is_admin() or request.user == event.created_by):
        return HttpResponseForbidden("You can only edit your own events.")
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Event "{event.title}" updated.')
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event, user=request.user)
    return render(request, 'events/event_form.html', {'form': form, 'action': 'Edit', 'event': event})


# Allows the event creator or an admin to delete an event.
# Shows a confirmation page on GET; performs the delete on POST.
@login_required
def event_delete_view(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if not (request.user.is_admin() or request.user == event.created_by):
        return HttpResponseForbidden("You can only delete your own events.")
    if request.method == 'POST':
        title = event.title
        event.delete()
        messages.success(request, f'Event "{title}" deleted.')
        return redirect('event_list')
    return render(request, 'events/event_delete_confirm.html', {'event': event})


# Registers the current user for an event. Blocks duplicate registrations
# and prevents registration when the event has reached max capacity.
@login_required
def event_register_view(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        if EventRegistration.objects.filter(event=event, user=request.user).exists():
            messages.warning(request, "You are already registered for this event.")
        elif event.is_full():
            messages.error(request, "This event is full. No spots available.")
        else:
            EventRegistration.objects.create(event=event, user=request.user)
            messages.success(request, f'Successfully registered for "{event.title}"!')
    return redirect('event_detail', pk=pk)


# Cancels the current user's registration for an event.
@login_required
def event_cancel_registration_view(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        registration = EventRegistration.objects.filter(event=event, user=request.user).first()
        if registration:
            registration.delete()
            messages.success(request, f'Registration for "{event.title}" cancelled.')
        else:
            messages.warning(request, "You are not registered for this event.")
    return redirect('event_detail', pk=pk)
