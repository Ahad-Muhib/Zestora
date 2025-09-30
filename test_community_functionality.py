#!/usr/bin/env python
"""
Test script to verify community functionality
"""
import os
import django
import requests

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zestora.settings')
django.setup()

from django.contrib.auth.models import User
from recipes.models import Recipe

def test_community_functionality():
    """Test all community pages and functionality"""
    print("🧪 Testing Community Functionality...")
    
    base_url = "http://127.0.0.1:8001"
    
    # Test pages
    test_urls = [
        ("/community/", "Community Home"),
        ("/community/members/", "Community Members"),
    ]
    
    # Test community pages
    for url, name in test_urls:
        full_url = f"{base_url}{url}"
        try:
            response = requests.get(full_url, timeout=10)
            if response.status_code == 200:
                print(f"   ✅ {name}: OK (200)")
            else:
                print(f"   ❌ {name}: {response.status_code}")
        except requests.RequestException as e:
            print(f"   ❌ {name} error: {e}")
    
    # Test user profiles
    print(f"\n👥 Testing User Profiles...")
    users_with_recipes = User.objects.filter(recipe__isnull=False).distinct()[:3]
    
    for user in users_with_recipes:
        recipe_count = Recipe.objects.filter(author=user).count()
        profile_url = f"{base_url}/community/profile/{user.id}/"
        
        try:
            response = requests.get(profile_url, timeout=10)
            if response.status_code == 200:
                print(f"   ✅ {user.username} profile: OK ({recipe_count} recipes)")
            else:
                print(f"   ❌ {user.username} profile: {response.status_code}")
        except requests.RequestException as e:
            print(f"   ❌ {user.username} profile error: {e}")
    
    print(f"\n🎉 Community functionality testing complete!")
    
    # Print community stats
    print(f"\n📊 Community Statistics:")
    total_users = User.objects.count()
    users_with_recipes_count = User.objects.filter(recipe__isnull=False).distinct().count()
    total_recipes = Recipe.objects.count()
    
    print(f"   👤 Total Users: {total_users}")
    print(f"   🍽️ Users with Recipes: {users_with_recipes_count}")
    print(f"   📝 Total Recipes: {total_recipes}")
    print(f"   📈 Community Engagement: {(users_with_recipes_count/total_users*100):.1f}%")

if __name__ == "__main__":
    test_community_functionality()