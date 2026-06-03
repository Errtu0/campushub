from django.contrib import admin
from .models import Club

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ['name', 'manager', 'status', 'member_count', 'created_at']
    list_filter = ['status']
    search_fields = ['name']
