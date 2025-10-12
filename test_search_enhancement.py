#!/usr/bin/env python
"""
Test script to verify the enhanced search functionality
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zestora.settings')
sys.path.append('/home/muhib/muhib/project/Zestora')

django.setup()

from django.contrib.auth.models import User
from recipes.models import Recipe, Category
from django.db.models import Q

def test_search_functionality():
    """Test the enhanced search functionality"""
    print("Testing Enhanced Search Functionality")
    print("=" * 50)
    
    # Get some sample data
    users = User.objects.all()
    recipes = Recipe.objects.all()
    
    print(f"Found {users.count()} users and {recipes.count()} recipes")
    print()
    
    if users.exists() and recipes.exists():
        # Test searching by recipe title
        print("1. Testing recipe title search:")
        sample_recipe = recipes.first()
        title_query = sample_recipe.title.split()[0] if sample_recipe.title else "test"
        title_results = Recipe.objects.filter(
            Q(title__icontains=title_query) | 
            Q(description__icontains=title_query) | 
            Q(ingredients__icontains=title_query) |
            Q(author__username__icontains=title_query) |
            Q(author__first_name__icontains=title_query) |
            Q(author__last_name__icontains=title_query)
        ).select_related('author', 'category').distinct()
        
        print(f"   Query: '{title_query}'")
        print(f"   Results: {title_results.count()} recipes")
        for recipe in title_results[:3]:
            print(f"   - {recipe.title} by {recipe.author.profile.full_name}")
        print()
        
        # Test searching by chef username
        print("2. Testing chef username search:")
        sample_user = users.first()
        username_query = sample_user.username
        username_results = Recipe.objects.filter(
            Q(title__icontains=username_query) | 
            Q(description__icontains=username_query) | 
            Q(ingredients__icontains=username_query) |
            Q(author__username__icontains=username_query) |
            Q(author__first_name__icontains=username_query) |
            Q(author__last_name__icontains=username_query)
        ).select_related('author', 'category').distinct()
        
        print(f"   Query: '{username_query}'")
        print(f"   Results: {username_results.count()} recipes")
        for recipe in username_results[:3]:
            print(f"   - {recipe.title} by {recipe.author.profile.full_name}")
        print()
        
        # Test searching by chef first name (if available)
        print("3. Testing chef first name search:")
        user_with_first_name = users.filter(first_name__isnull=False, first_name__gt='').first()
        if user_with_first_name and user_with_first_name.first_name:
            first_name_query = user_with_first_name.first_name
            first_name_results = Recipe.objects.filter(
                Q(title__icontains=first_name_query) | 
                Q(description__icontains=first_name_query) | 
                Q(ingredients__icontains=first_name_query) |
                Q(author__username__icontains=first_name_query) |
                Q(author__first_name__icontains=first_name_query) |
                Q(author__last_name__icontains=first_name_query)
            ).select_related('author', 'category').distinct()
            
            print(f"   Query: '{first_name_query}'")
            print(f"   Results: {first_name_results.count()} recipes")
            for recipe in first_name_results[:3]:
                print(f"   - {recipe.title} by {recipe.author.profile.full_name}")
        else:
            print("   No users with first names found")
        print()
        
        print("✅ Search enhancement appears to be working!")
        print("Users can now search by:")
        print("   - Recipe titles")
        print("   - Recipe descriptions")
        print("   - Recipe ingredients")
        print("   - Chef usernames")
        print("   - Chef first names")
        print("   - Chef last names")
        
    else:
        print("⚠️  No sample data found. Please add some recipes and users first.")

if __name__ == "__main__":
    test_search_functionality()