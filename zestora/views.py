from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
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
        'active_page': 'home',
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
    
    context = results.copy()
    context['active_page'] = 'search'
    return render(request, 'search_results.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            # Try to authenticate with username first
            user = authenticate(request, username=username, password=password)
            
            # If that fails, try to find user by email
            if user is None:
                try:
                    user_obj = User.objects.get(email=username)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username/email or password.')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'login.html', {'active_page': 'login'})

def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        contact = request.POST.get('contact')
        password = request.POST.get('password')
        
        if email and username and password:
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Username "{username}" already exists. Please choose a different one.')
                return render(request, 'signup.html', {'active_page': 'signup'})
            # Check if email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, f'Email "{email}" already exists. Please use a different email.')
                return render(request, 'signup.html', {'active_page': 'signup'})
            
            try:
                # Create new user
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                
                # Log the user in automatically with the correct backend
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, f'Welcome to Zestora, {username}! Your account has been created successfully.')
                return redirect('home')
            except Exception as e:
                # More specific error messages based on the exception
                print(f"Signup error: {str(e)}")  # Log the actual error
                error_message = str(e).lower()
                if 'password' in error_message:
                    messages.error(request, 'Password does not meet security requirements. Please choose a stronger password.')
                elif 'username' in error_message:
                    messages.error(request, 'Invalid username format. Please try a different username.')
                elif 'email' in error_message:
                    messages.error(request, 'Invalid email format. Please check your email address.')
                else:
                    messages.error(request, f'An error occurred while creating your account: {str(e)}')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'signup.html', {'active_page': 'signup'})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

def guidebooks(request):
    return render(request, 'guidebooks.html', {'active_page': 'guidebooks'})

def about(request):
    return render(request, 'about.html', {'active_page': 'about'})