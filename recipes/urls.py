from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    path('add/', views.add_recipe, name='add_recipe'),
    path('categories/', views.category_list, name='category_list'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('<slug:slug>/', views.recipe_detail, name='recipe_detail'),
]