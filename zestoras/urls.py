from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # homepage
    path('hometest/', views.hometest, name='hometest'),  # test page


    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path('recipe1/', views.recipe_view, name='recipe1'), 
]
