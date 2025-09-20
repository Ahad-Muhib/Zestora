from django.urls import path
from . import views

app_name = 'tips'

urlpatterns = [
    path('', views.tip_list, name='tip_list'),
    path('category/<slug:slug>/', views.tip_category, name='tip_category'),
    path('<slug:slug>/', views.tip_detail, name='tip_detail'),
]