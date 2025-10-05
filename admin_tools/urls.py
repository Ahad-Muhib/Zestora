from django.urls import path
from . import views

app_name = 'admin_tools'

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='dashboard'),
    path('users/', views.manage_users, name='manage_users'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('toggle-user-status/', views.toggle_user_status, name='toggle_user_status'),
    path('system/', views.system_tools, name='system_tools'),
]