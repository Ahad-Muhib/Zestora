from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import CulinaryStory, UserProfile
from django.contrib.auth.models import User
from recipes.models import Recipe

def community_home(request):
    # Get recent users (those who have recipes)
    recent_users = User.objects.filter(recipe__isnull=False).distinct().order_by('-date_joined')[:12]
    
    # Get featured stories
    featured_stories = CulinaryStory.objects.filter(featured=True)[:6]
    
    # Get recent recipes from community
    recent_recipes = Recipe.objects.select_related('author', 'category').order_by('-created_at')[:8]
    
    return render(request, 'community/community_home.html', {
        'recent_users': recent_users,
        'featured_stories': featured_stories,
        'recent_recipes': recent_recipes,
        'active_page': 'community'
    })

def story_list(request):
    stories = CulinaryStory.objects.all().order_by('-created_at')
    return render(request, 'community/story_list.html', {'stories': stories, 'active_page': 'community'})

def story_detail(request, slug):
    story = get_object_or_404(CulinaryStory, slug=slug)
    return render(request, 'community/story_detail.html', {'story': story, 'active_page': 'community'})

def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        profile = None
    
    # Get user's recipes
    user_recipes = Recipe.objects.filter(author=user).order_by('-created_at')
    
    # Pagination for recipes
    paginator = Paginator(user_recipes, 12)  # Show 12 recipes per page
    page_number = request.GET.get('page')
    recipes_page = paginator.get_page(page_number)
    
    # Get user's cooking stats
    recipe_count = user_recipes.count()
    total_likes = 0
    for recipe in user_recipes:
        try:
            total_likes += recipe.likes.filter(is_like=True).count()
        except:
            total_likes += 0
    
    return render(request, 'community/user_profile.html', {
        'profile_user': user, 
        'profile': profile, 
        'recipes_page': recipes_page,
        'recipe_count': recipe_count,
        'total_likes': total_likes,
        'active_page': 'community'
    })

def community_members(request):
    """Display all community members who have created recipes"""
    # Get users who have created at least one recipe
    users_with_recipes = User.objects.filter(recipe__isnull=False).distinct().order_by('-date_joined')
    
    # Add recipe count to each user
    users_data = []
    for user in users_with_recipes:
        recipe_count = Recipe.objects.filter(author=user).count()
        latest_recipe = Recipe.objects.filter(author=user).order_by('-created_at').first()
        
        try:
            profile = user.userprofile
        except UserProfile.DoesNotExist:
            profile = None
            
        users_data.append({
            'user': user,
            'profile': profile,
            'recipe_count': recipe_count,
            'latest_recipe': latest_recipe
        })
    
    # Pagination
    paginator = Paginator(users_data, 16)  # Show 16 members per page
    page_number = request.GET.get('page')
    users_page = paginator.get_page(page_number)
    
    return render(request, 'community/members.html', {
        'users_page': users_page,
        'total_members': len(users_data),
        'active_page': 'community'
    })
