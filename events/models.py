from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from clubs.models import Club


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='events')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_events'
    )
    location = models.CharField(max_length=300)
    date = models.DateTimeField()
    max_participants = models.PositiveIntegerField(default=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.title} - {self.club.name}"

    def participant_count(self):
        return self.registrations.count()

    def is_full(self):
        return self.registrations.count() >= self.max_participants

    def spots_left(self):
        return max(0, self.max_participants - self.registrations.count())


class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='event_registrations'
    )
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')
        ordering = ['registered_at']

    def __str__(self):
        return f"{self.user.username} -> {self.event.title}"

    def clean(self):
        if self.event.is_full():
            raise ValidationError("This event is full. No more spots available.")
