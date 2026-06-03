from django.contrib import admin
from .models import Event, EventRegistration

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'club', 'date', 'participant_count', 'max_participants']

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['event', 'user', 'registered_at']
