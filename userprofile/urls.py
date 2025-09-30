from django.urls import path
from . import views

app_name = 'userprofile'

urlpatterns = [
    path('', views.profile_view, name='profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('<str:username>/', views.profile_view, name='profile'),
]
