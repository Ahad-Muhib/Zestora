#!/usr/bin/env python
import os
import sys
import django

# Setup Django
if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zestora.settings')
    django.setup()
    
    from django.contrib.auth.models import User
    
    # Create admin user if it doesn't exist
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@zestora.com',
            password='admin123'
        )
        print("✅ Admin user created successfully!")
        print("Username: admin")
        print("Password: admin123") 
        print("Email: admin@zestora.com")
    else:
        print("❌ Admin user already exists!")
        admin_user = User.objects.get(username='admin')
        print(f"Username: {admin_user.username}")
        print(f"Email: {admin_user.email}")
        print(f"Is Staff: {admin_user.is_staff}")
        print(f"Is Superuser: {admin_user.is_superuser}")