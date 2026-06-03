from django.urls import path
from . import views

urlpatterns = [
    path('', views.club_list_view, name='club_list'),
    path('create/', views.club_create_view, name='club_create'),
    path('<int:pk>/', views.club_detail_view, name='club_detail'),
    path('<int:pk>/edit/', views.club_edit_view, name='club_edit'),
    path('<int:pk>/join/', views.club_join_view, name='club_join'),
    path('<int:pk>/leave/', views.club_leave_view, name='club_leave'),
    path('<int:pk>/delete/', views.admin_club_delete, name='admin_club_delete'),
    path('dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('admin/approval/', views.admin_club_approval, name='admin_club_approval'),
    path('admin/approve/<int:pk>/', views.admin_club_approve, name='admin_club_approve'),
]
