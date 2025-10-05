from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from recipes.models import Recipe, Comment, RecipeLike, Category
from userprofile.models import UserProfile
from community.models import CulinaryStory


def is_admin(user):
    """Check if user is admin or staff"""
    return user.is_authenticated and (user.is_staff or user.is_superuser)


@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard with statistics overview"""
    # Basic counts
    total_users = User.objects.count()
    total_recipes = Recipe.objects.count()
    total_comments = Comment.objects.count()
    total_likes = RecipeLike.objects.filter(is_like=True).count()
    total_dislikes = RecipeLike.objects.filter(is_like=False).count()
    total_categories = Category.objects.count()
    
    # Recent activity (last 7 days)
    week_ago = timezone.now() - timedelta(days=7)
    new_users_week = User.objects.filter(date_joined__gte=week_ago).count()
    new_recipes_week = Recipe.objects.filter(created_at__gte=week_ago).count()
    new_comments_week = Comment.objects.filter(created_at__gte=week_ago).count()
    
    # Most active users (by recipe count)
    most_active_users = User.objects.annotate(
        recipe_count=Count('recipe')
    ).filter(recipe_count__gt=0).order_by('-recipe_count')[:10]
    
    # Most popular recipes (by total likes)
    popular_recipes = Recipe.objects.annotate(
        total_likes=Count('likes', filter=Q(likes__is_like=True))
    ).order_by('-total_likes')[:10]
    
    # Recent users
    recent_users = User.objects.order_by('-date_joined')[:10]
    
    # Categories with recipe counts
    categories_stats = Category.objects.annotate(
        recipe_count=Count('recipe')
    ).order_by('-recipe_count')
    
    context = {
        'total_users': total_users,
        'total_recipes': total_recipes,
        'total_comments': total_comments,
        'total_likes': total_likes,
        'total_dislikes': total_dislikes,
        'total_categories': total_categories,
        'new_users_week': new_users_week,
        'new_recipes_week': new_recipes_week,
        'new_comments_week': new_comments_week,
        'most_active_users': most_active_users,
        'popular_recipes': popular_recipes,
        'recent_users': recent_users,
        'categories_stats': categories_stats,
        'active_page': 'admin',
    }
    
    return render(request, 'admin_tools/dashboard.html', context)


@user_passes_test(is_admin)
def manage_users(request):
    """Manage users page with search and filters"""
    users_queryset = User.objects.all().order_by('-date_joined')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        users_queryset = users_queryset.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    # Filter by user type
    user_type = request.GET.get('type', '')
    if user_type == 'admin':
        users_queryset = users_queryset.filter(Q(is_staff=True) | Q(is_superuser=True))
    elif user_type == 'active':
        users_queryset = users_queryset.filter(is_active=True)
    elif user_type == 'inactive':
        users_queryset = users_queryset.filter(is_active=False)
    
    # Add user statistics
    users_with_stats = []
    for user in users_queryset:
        recipe_count = Recipe.objects.filter(author=user).count()
        comment_count = Comment.objects.filter(author=user).count()
        likes_given = RecipeLike.objects.filter(user=user, is_like=True).count()
        
        try:
            profile = user.userprofile
        except UserProfile.DoesNotExist:
            profile = None
            
        users_with_stats.append({
            'user': user,
            'profile': profile,
            'recipe_count': recipe_count,
            'comment_count': comment_count,
            'likes_given': likes_given,
        })
    
    # Pagination
    paginator = Paginator(users_with_stats, 20)
    page_number = request.GET.get('page')
    users_page = paginator.get_page(page_number)
    
    context = {
        'users_page': users_page,
        'search_query': search_query,
        'user_type': user_type,
        'total_users': User.objects.count(),
        'active_page': 'admin',
    }
    
    return render(request, 'admin_tools/manage_users.html', context)


@user_passes_test(is_admin)
@require_POST
def toggle_user_status(request, user_id):
    """Toggle user active status"""
    user = get_object_or_404(User, id=user_id)
    
    if user == request.user:
        return JsonResponse({'error': 'Cannot deactivate yourself'}, status=400)
    
    if user.is_superuser and not request.user.is_superuser:
        return JsonResponse({'error': 'Cannot modify superuser'}, status=403)
    
    user.is_active = not user.is_active
    user.save()
    
    action = 'activated' if user.is_active else 'deactivated'
    return JsonResponse({
        'success': True,
        'message': f'User {user.username} has been {action}',
        'is_active': user.is_active
    })


@user_passes_test(is_admin)
def system_tools(request):
    """System tools and maintenance"""
    # System stats
    total_files = 0
    
    # Count uploaded files (recipes, profiles)
    recipe_images = Recipe.objects.exclude(image='').count()
    profile_images = UserProfile.objects.exclude(profile_image='').count()
    
    # Database stats
    db_stats = {
        'users': User.objects.count(),
        'recipes': Recipe.objects.count(),
        'comments': Comment.objects.count(),
        'likes': RecipeLike.objects.count(),
        'categories': Category.objects.count(),
        'profiles': UserProfile.objects.count(),
        'stories': CulinaryStory.objects.count(),
    }
    
    # Recent activity
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    activity_stats = {
        'users_today': User.objects.filter(date_joined__date=today).count(),
        'users_week': User.objects.filter(date_joined__date__gte=week_ago).count(),
        'users_month': User.objects.filter(date_joined__date__gte=month_ago).count(),
        'recipes_today': Recipe.objects.filter(created_at__date=today).count(),
        'recipes_week': Recipe.objects.filter(created_at__date__gte=week_ago).count(),
        'recipes_month': Recipe.objects.filter(created_at__date__gte=month_ago).count(),
    }
    
    context = {
        'db_stats': db_stats,
        'activity_stats': activity_stats,
        'recipe_images': recipe_images,
        'profile_images': profile_images,
        'total_files': recipe_images + profile_images,
        'active_page': 'admin',
    }
    
    return render(request, 'admin_tools/system_tools.html', context)


@user_passes_test(is_admin)
def user_detail(request, user_id):
    """Detailed view of a specific user"""
    user = get_object_or_404(User, id=user_id)
    
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        profile = None
    
    # User's recipes
    recipes = Recipe.objects.filter(author=user).order_by('-created_at')
    
    # User's comments
    comments = Comment.objects.filter(author=user).order_by('-created_at')[:10]
    
    # User's likes/dislikes
    likes = RecipeLike.objects.filter(user=user, is_like=True).order_by('-created_at')[:10]
    dislikes = RecipeLike.objects.filter(user=user, is_like=False).order_by('-created_at')[:10]
    
    # Statistics
    stats = {
        'total_recipes': recipes.count(),
        'total_comments': Comment.objects.filter(author=user).count(),
        'total_likes_given': RecipeLike.objects.filter(user=user, is_like=True).count(),
        'total_dislikes_given': RecipeLike.objects.filter(user=user, is_like=False).count(),
        'total_likes_received': sum(recipe.likes_count for recipe in recipes),
        'total_comments_received': sum(Comment.objects.filter(recipe=recipe).count() for recipe in recipes),
    }
    
    context = {
        'profile_user': user,
        'profile': profile,
        'recipes': recipes[:10],  # Show only first 10
        'recent_comments': comments,
        'recent_likes': likes,
        'recent_dislikes': dislikes,
        'stats': stats,
        'active_page': 'admin',
    }
    
    return render(request, 'admin_tools/user_detail.html', context)
