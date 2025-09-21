from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recipes.models import Recipe, Category

class Command(BaseCommand):
    help = 'Add test data for search functionality'

    def handle(self, *args, **options):
        # Create a test user
        user, created = User.objects.get_or_create(
            username='test_chef',
            defaults={
                'first_name': 'Test',
                'last_name': 'Chef',
                'email': 'test@zestora.com'
            }
        )
        self.stdout.write(f'User created: {created}')
        
        # Create a test category
        category, created = Category.objects.get_or_create(
            slug='dinner',
            defaults={
                'name': 'Dinner',
                'description': 'Evening meals and main courses'
            }
        )
        self.stdout.write(f'Category created: {created}')
        
        # Create a test recipe
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
        self.stdout.write(f'Recipe created: {created}')
        
        self.stdout.write(
            self.style.SUCCESS('Test data added successfully!')
        )
