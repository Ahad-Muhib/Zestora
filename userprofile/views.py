from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .models import UserProfile
from recipes.models import Recipe

@login_required
def profile_view(request, username=None):
    """View user profile with tabs"""
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    
    profile = user.profile
    user_recipes = Recipe.objects.filter(author=user).order_by('-created_at')
    
    # Get saved recipes
    from recipes.models import SavedRecipe
    saved_recipe_ids = SavedRecipe.objects.filter(user=user).values_list('recipe_id', flat=True)
    saved_recipes = Recipe.objects.filter(id__in=saved_recipe_ids).order_by('-created_at')
    
    context = {
        'profile_user': user,
        'profile': profile,
        'user_recipes': user_recipes,
        'saved_recipes': saved_recipes,
        'is_own_profile': request.user == user,
        'active_page': 'profile',
    }
    return render(request, 'userprofile/profile.html', context)

@login_required
def edit_profile(request):
    """Edit user profile information"""
    profile = request.user.profile
    
    if request.method == 'POST':
        # Update user fields
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        
        # Update profile fields
        profile.bio = request.POST.get('bio', '')
        profile.location = request.POST.get('location', '')
        profile.phone = request.POST.get('phone', '')
        profile.website = request.POST.get('website', '')
        
        # Handle profile image upload
        if 'profile_image' in request.FILES:
            profile.profile_image = request.FILES['profile_image']
        
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('userprofile:profile', username=request.user.username)
    
    return redirect('userprofile:profile', username=request.user.username)

@login_required
def change_password(request):
    """Change user password"""
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
        elif new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
        elif len(new_password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
        else:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)  # Keep user logged in
            messages.success(request, 'Password changed successfully!')
    
    return redirect('userprofile:profile', username=request.user.username)
