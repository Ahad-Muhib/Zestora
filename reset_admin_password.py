from django.contrib.auth.models import User

# Get admin user and set password
admin_user = User.objects.get(username='admin')
admin_user.set_password('admin123')
admin_user.save()

print("✅ Admin password reset to 'admin123'")
print(f"Username: {admin_user.username}")
print(f"Is Staff: {admin_user.is_staff}")
print(f"Is Superuser: {admin_user.is_superuser}")