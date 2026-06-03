from django.db import models
from django.conf import settings


class Club(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    logo = models.ImageField(upload_to='club_logos/', blank=True, null=True)
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='managed_clubs'
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='joined_clubs',
        blank=True
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def is_approved(self):
        return self.status == 'approved'

    def member_count(self):
        return self.members.count()
