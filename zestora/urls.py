"""
URL configuration for zestora project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('community/', include('community.urls')),
    path('tips/', include('tips.urls')),
    path('search/', views.search, name='search'),
    path('guidebooks/', views.guidebooks, name='guidebooks'),
    path('about/', views.about, name='about'),
    path('logout/', views.logout_view, name='logout'),

    # Custom auth views
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    
    # Django Allauth URLs
    path('accounts/', include('allauth.urls')),
    
    path('recipes/', include('recipes.urls')),
    path('profile/', include('userprofile.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)