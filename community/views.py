from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import CulinaryStory, UserProfile
from django.contrib.auth.models import User

def community_home(request):
    featured_stories = CulinaryStory.objects.filter(featured=True)[:6]
    return render(request, 'community/community_home.html', {'featured_stories': featured_stories})

def story_list(request):
    stories = CulinaryStory.objects.all().order_by('-created_at')
    return render(request, 'community/story_list.html', {'stories': stories})

def story_detail(request, slug):
    story = get_object_or_404(CulinaryStory, slug=slug)
    return render(request, 'community/story_detail.html', {'story': story})

def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        profile = None
    return render(request, 'community/user_profile.html', {'profile_user': user, 'profile': profile})
