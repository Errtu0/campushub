from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('club_manager', 'Club Manager'),
        ('admin', 'Admin'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    student_id = models.CharField(max_length=20, blank=True)

    # Role helpers used throughout views and templates for permission checks.
    def is_student(self):
        return self.role == 'student'

    def is_club_manager(self):
        return self.role == 'club_manager'

    # Also returns True for Django superusers so createsuperuser accounts
    # get full admin access without needing the role field set manually.
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
