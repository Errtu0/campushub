from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list_view, name='event_list'),
    path('create/', views.event_create_view, name='event_create'),
    path('<int:pk>/', views.event_detail_view, name='event_detail'),
    path('<int:pk>/edit/', views.event_edit_view, name='event_edit'),
    path('<int:pk>/delete/', views.event_delete_view, name='event_delete'),
    path('<int:pk>/register/', views.event_register_view, name='event_register'),
    path('<int:pk>/cancel/', views.event_cancel_registration_view, name='event_cancel'),
]
