from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import Q, Count
from recipes.models import Recipe, RecipeLike, Comment
from userprofile.models import UserProfile
import json


def is_admin(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_admin)
def admin_dashboard(request):
    # Get statistics
    total_users = User.objects.count()
    total_recipes = Recipe.objects.count()
    total_comments = Comment.objects.count()
    total_likes = RecipeLike.objects.count()
    
    # Recent activity
    recent_users = User.objects.order_by('-date_joined')[:5]
    recent_recipes = Recipe.objects.order_by('-created_at')[:5]
    recent_comments = Comment.objects.order_by('-created_at')[:5]
    
    # Top recipes by likes
    top_recipes = Recipe.objects.all()
    top_recipes_with_likes = []
    for recipe in top_recipes:
        like_count = recipe.likes.filter(is_like=True).count()
        top_recipes_with_likes.append({
            'recipe': recipe,
            'like_count': like_count
        })
    
    # Sort by like count and take top 5
    top_recipes_with_likes.sort(key=lambda x: x['like_count'], reverse=True)
    top_recipes_data = top_recipes_with_likes[:5]
    
    context = {
        'total_users': total_users,
        'total_recipes': total_recipes,
        'total_comments': total_comments,
        'total_likes': total_likes,
        'recent_users': recent_users,
        'recent_recipes': recent_recipes,
        'recent_comments': recent_comments,
        'top_recipes': top_recipes_data,
    }
    
    return render(request, 'admin_tools/dashboard.html', context)


@user_passes_test(is_admin)
def manage_users(request):
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', 'all')
    
    users = User.objects.all()
    
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    if status_filter == 'active':
        users = users.filter(is_active=True)
    elif status_filter == 'inactive':
        users = users.filter(is_active=False)
    elif status_filter == 'staff':
        users = users.filter(is_staff=True)
    
    users = users.order_by('-date_joined')
    
    # Prepare user data with statistics
    users_data = []
    for user in users:
        # Safely get user profile using getattr with default None
        user_profile = getattr(user, 'userprofile', None)
        
        user_recipes = Recipe.objects.filter(author=user).count()
        user_comments = Comment.objects.filter(user=user).count()
        
        users_data.append({
            'user': user,
            'profile': user_profile,
            'recipe_count': user_recipes,
            'comment_count': user_comments,
        })
    
    context = {
        'users_data': users_data,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    
    return render(request, 'admin_tools/manage_users.html', context)


@user_passes_test(is_admin)
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    # Safely get user profile using getattr with default None
    user_profile = getattr(user, 'userprofile', None)
    
    user_recipes = Recipe.objects.filter(author=user)
    user_comments = Comment.objects.filter(user=user)
    user_likes = RecipeLike.objects.filter(user=user)
    
    context = {
        'user_detail': user,
        'profile': user_profile,
        'user_recipes': user_recipes,
        'user_comments': user_comments,
        'user_likes': user_likes,
    }
    
    return render(request, 'admin_tools/user_detail.html', context)


@user_passes_test(is_admin)
@require_POST
def toggle_user_status(request):
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        user = get_object_or_404(User, id=user_id)
        
        user.is_active = not user.is_active
        user.save()
        
        return JsonResponse({
            'success': True,
            'is_active': user.is_active,
            'message': f'User {"activated" if user.is_active else "deactivated"} successfully'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })


@user_passes_test(is_admin)
def system_tools(request):
    import platform
    import sys
    import django
    from django.conf import settings
    
    system_info = {
        'python_version': sys.version,
        'django_version': django.get_version(),
        'platform': platform.platform(),
        'debug_mode': settings.DEBUG,
        'database_engine': settings.DATABASES['default']['ENGINE'],
    }
    
    context = {
        'system_info': system_info,
    }
    
    return render(request, 'admin_tools/system_tools.html', context)
