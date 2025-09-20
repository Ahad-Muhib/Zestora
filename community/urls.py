from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.community_home, name='community_home'),
    path('stories/', views.story_list, name='story_list'),
    path('story/<slug:slug>/', views.story_detail, name='story_detail'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
]