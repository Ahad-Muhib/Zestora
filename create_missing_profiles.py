#!/usr/bin/env python
"""
Create missing user profiles for existing users
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zestora.settings')
sys.path.append('/home/muhib/muhib/project/Zestora')

django.setup()

from django.contrib.auth.models import User
from userprofile.models import UserProfile

def create_missing_profiles():
    """Create profiles for users who don't have them"""
    print("Creating missing user profiles...")
    print("=" * 40)
    
    users_without_profiles = []
    
    for user in User.objects.all():
        try:
            # Try to access the profile
            profile = user.profile
        except UserProfile.DoesNotExist:
            # Create missing profile
            profile = UserProfile.objects.create(user=user)
            users_without_profiles.append(user.username)
            print(f"✅ Created profile for user: {user.username}")
    
    if not users_without_profiles:
        print("ℹ️  All users already have profiles!")
    else:
        print(f"\n✅ Created {len(users_without_profiles)} missing profiles")
        print("Users that received new profiles:")
        for username in users_without_profiles:
            print(f"  - {username}")

if __name__ == "__main__":
    create_missing_profiles()