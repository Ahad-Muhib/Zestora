from django.contrib.auth.models import User

if not User.objects.filter(username='testuser').exists():
    User.objects.create_user('testuser', 'test@example.com', 'test123')
    print('Regular user created: testuser / test123')
else:
    print('Test user already exists')