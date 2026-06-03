from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from events.models import Event
from clubs.models import Club


def home_view(request):
    recent_events = Event.objects.filter(club__status='approved').order_by('date')[:6]
    approved_clubs = Club.objects.filter(status='approved')[:6]
    return render(request, 'home.html', {
        'recent_events': recent_events,
        'approved_clubs': approved_clubs,
    })


urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('clubs/', include('clubs.urls')),
    path('events/', include('events.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
