#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zestora.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def test_admin_tools():
    print("🧪 Testing Admin Tools...")
    
    # Get admin user
    try:
        admin_user = User.objects.get(username='admin')
        print(f"✅ Admin user found: {admin_user.username}")
        print(f"   - Is Staff: {admin_user.is_staff}")
        print(f"   - Is Superuser: {admin_user.is_superuser}")
    except User.DoesNotExist:
        print("❌ Admin user not found")
        return
    
    # Create a client and login
    client = Client()
    login_success = client.login(username='admin', password='admin123')
    
    if login_success:
        print("✅ Admin login successful")
        
        # Test dashboard
        print("\n📊 Testing Dashboard...")
        response = client.get('/admin-tools/dashboard/')
        if response.status_code == 200:
            print("✅ Dashboard loads successfully")
            print(f"   - Status Code: {response.status_code}")
        else:
            print(f"❌ Dashboard failed - Status Code: {response.status_code}")
        
        # Test manage users
        print("\n👥 Testing Manage Users...")
        response = client.get('/admin-tools/users/')
        if response.status_code == 200:
            print("✅ Manage Users loads successfully")
            print(f"   - Status Code: {response.status_code}")
        else:
            print(f"❌ Manage Users failed - Status Code: {response.status_code}")
        
        # Test system tools
        print("\n🔧 Testing System Tools...")
        response = client.get('/admin-tools/system/')
        if response.status_code == 200:
            print("✅ System Tools loads successfully")
            print(f"   - Status Code: {response.status_code}")
        else:
            print(f"❌ System Tools failed - Status Code: {response.status_code}")
            
    else:
        print("❌ Admin login failed")
        
    # Test statistics data
    print("\n📈 Testing Statistics Data...")
    from recipes.models import Recipe, Comment, RecipeLike
    
    try:
        total_users = User.objects.count()
        total_recipes = Recipe.objects.count()
        total_comments = Comment.objects.count()
        total_likes = RecipeLike.objects.count()
        
        print(f"✅ Statistics gathered successfully:")
        print(f"   - Total Users: {total_users}")
        print(f"   - Total Recipes: {total_recipes}")
        print(f"   - Total Comments: {total_comments}")
        print(f"   - Total Likes: {total_likes}")
        
    except Exception as e:
        print(f"❌ Statistics gathering failed: {e}")

if __name__ == "__main__":
    test_admin_tools()