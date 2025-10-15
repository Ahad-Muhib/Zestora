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
    
    # Get search suggestions for autocomplete
    suggestions = []
    if query and len(query) >= 2:
        # Get recipe title suggestions
        recipe_suggestions = Recipe.objects.filter(
            title__icontains=query
        ).values_list('title', flat=True)[:5]
        
        # Get chef name suggestions
        chef_suggestions = User.objects.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) |
            Q(username__icontains=query)
        ).exclude(first_name='', last_name='').values_list('first_name', 'last_name')[:3]
        
        # Format chef names
        chef_names = [f"{first} {last}".strip() for first, last in chef_suggestions if first or last]
        
        # Get ingredient suggestions
        ingredient_suggestions = Recipe.objects.filter(
            ingredients__icontains=query
        ).values_list('ingredients', flat=True)[:3]
        
        # Extract unique ingredient words
        ingredient_words = set()
        for ingredients in ingredient_suggestions:
            words = [word.strip().lower() for word in ingredients.split(',')]
            for word in words:
                if query.lower() in word.lower() and len(word) > 2:
                    ingredient_words.add(word.title())
        
        suggestions = list(recipe_suggestions) + chef_names + list(ingredient_words)[:10]
    
    # Handle search history (store in session)
    if query and query.strip():
        search_history = request.session.get('search_history', [])
        query_clean = query.strip()
        
        # Remove if already exists to avoid duplicates
        if query_clean in search_history:
            search_history.remove(query_clean)
        
        # Add to beginning of list
        search_history.insert(0, query_clean)
        
        # Keep only last 10 searches
        search_history = search_history[:10]
        
        request.session['search_history'] = search_history
    
    # Get current search history
    search_history = request.session.get('search_history', [])
    
    if query:
        # Search across recipes, tips, and stories
        # Enhanced recipe search including chef/author name
        # Split query into words for better full name matching
        query_words = query.strip().split()
        
        # Build recipe search query
        recipe_query = Q()
        
        # Search in recipe fields
        recipe_query |= Q(title__icontains=query)
        recipe_query |= Q(description__icontains=query)
        recipe_query |= Q(ingredients__icontains=query)
        
        # Search in author fields
        recipe_query |= Q(author__username__icontains=query)
        recipe_query |= Q(author__first_name__icontains=query)
        recipe_query |= Q(author__last_name__icontains=query)
        
        # For multiple words, also search for combinations
        if len(query_words) >= 2:
            # Try to match "first last" name combinations
            for i in range(len(query_words) - 1):
                first_word = query_words[i]
                second_word = query_words[i + 1]
                
                # Match first name + last name
                recipe_query |= (
                    Q(author__first_name__icontains=first_word) & 
                    Q(author__last_name__icontains=second_word)
                )
                
                # Also try reverse order (last name + first name)
                recipe_query |= (
                    Q(author__first_name__icontains=second_word) & 
                    Q(author__last_name__icontains=first_word)
                )
        
        recipe_results = Recipe.objects.filter(recipe_query).select_related('author__profile', 'category').distinct()
        
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
    context['suggestions'] = suggestions
    context['search_history'] = search_history
    return render(request, 'search_results.html', context)

def search_suggestions(request):
    """API endpoint for search suggestions"""
    query = request.GET.get('q', '')
    suggestions = []
    
    if query and len(query) >= 2:
        # Get recipe title suggestions
        recipe_suggestions = Recipe.objects.filter(
            title__icontains=query
        ).values_list('title', flat=True)[:5]
        
        # Get chef name suggestions
        chef_suggestions = User.objects.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) |
            Q(username__icontains=query)
        ).exclude(first_name='', last_name='').values_list('first_name', 'last_name')[:3]
        
        # Format chef names
        chef_names = [f"{first} {last}".strip() for first, last in chef_suggestions if first or last]
        
        suggestions = list(recipe_suggestions) + chef_names
        suggestions = suggestions[:8]  # Limit to 8 suggestions
    
    return JsonResponse({'suggestions': suggestions})

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
                    # Get the first user with this email (in case of duplicates)
                    user_obj = User.objects.filter(email=username).first()
                    if user_obj:
                        user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass
                
                # If still no user found, try authenticating other users with same email
                if user is None:
                    users_with_email = User.objects.filter(email=username)
                    for user_obj in users_with_email:
                        user = authenticate(request, username=user_obj.username, password=password)
                        if user:
                            break
            
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