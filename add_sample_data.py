import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zestora.settings')
django.setup()

from django.contrib.auth.models import User
from recipes.models import Recipe, Category

# Create a user
user, created = User.objects.get_or_create(
    username='test_chef',
    defaults={
        'first_name': 'Test',
        'last_name': 'Chef',
        'email': 'test@zestora.com'
    }
)

# Create a category
category, created = Category.objects.get_or_create(
    slug='dinner',
    defaults={
        'name': 'Dinner',
        'description': 'Evening meals and main courses'
    }
)

# Create a sample recipe
recipe, created = Recipe.objects.get_or_create(
    slug='test-chicken-recipe',
    defaults={
        'title': 'Test Chicken Recipe',
        'description': 'A delicious test chicken recipe for search testing',
        'ingredients': '2 lbs chicken, salt, pepper, herbs',
        'instructions': '1. Season chicken 2. Cook for 30 minutes 3. Serve hot',
        'prep_time': 10,
        'cook_time': 30,
        'servings': 4,
        'difficulty': 'easy',
        'category': category,
        'author': user
    }
)

print(f"Created user: {created}")
print(f"Created category: {created}")
print(f"Created recipe: {created}")
print("Sample data added successfully!")
