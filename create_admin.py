from django.contrib.auth.models import User

if not User.objects.filter(username='admin').exists():
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@zestora.com',
        password='admin123'
    )
    print("✅ Admin user created successfully!")
    print("Username: admin")
    print("Password: admin123")
else:
    print("❌ Admin user already exists!")
    admin_user = User.objects.get(username='admin')
    print(f"Username: {admin_user.username}")
    print(f"Email: {admin_user.email}")
    print(f"Is Staff: {admin_user.is_staff}")
    print(f"Is Superuser: {admin_user.is_superuser}")