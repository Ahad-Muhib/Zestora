from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.db.models import Q
from recipes.models import *
from community.models import *
from tips.models import *

def home(request):
    # Handle newsletter subscription
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            messages.success(request, 'Thank you for subscribing! You will receive weekly recipes and cooking tips.')
        return redirect('home')
    
    # Get featured recipes for homepage
    featured_recipes = Recipe.objects.filter(featured=True)[:4]
    
    return render(request, 'home.html', {
        'featured_recipes': featured_recipes,
    })

def search(request):
    query = request.GET.get('q', '')
    
    if query:
        # Search across recipes, tips, and stories
        recipe_results = Recipe.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) | 
            Q(ingredients__icontains=query)
        )
        
        tip_results = CookingTip.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) | 
            Q(short_description__icontains=query)
        )
        
        story_results = CulinaryStory.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query)
        )
        
        results = {
            'recipes': recipe_results,
            'tips': tip_results,
            'stories': story_results,
            'query': query
        }
    else:
        results = {
            'recipes': Recipe.objects.none(),
            'tips': CookingTip.objects.none(),
            'stories': CulinaryStory.objects.none(),
            'query': ''
        }
    
    return render(request, 'search_results.html', results)

def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')

def logout_view(request):
    return redirect('home')

def guidebooks(request):
    return render(request, 'guidebooks.html')

def about(request):
    return render(request, 'about.html')