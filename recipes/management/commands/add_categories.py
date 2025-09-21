from django.core.management.base import BaseCommand
from recipes.models import Category

class Command(BaseCommand):
    help = 'Add recipe categories to the database'

    def handle(self, *args, **options):
        categories_data = [
            {
                'name': 'Breakfast',
                'slug': 'breakfast',
                'description': 'Morning meals and brunch recipes to start your day right'
            },
            {
                'name': 'Lunch',
                'slug': 'lunch',
                'description': 'Midday meals and light dishes for a satisfying lunch'
            },
            {
                'name': 'Dinner',
                'slug': 'dinner',
                'description': 'Evening meals and main courses for the perfect dinner'
            },
            {
                'name': 'Dessert',
                'slug': 'dessert',
                'description': 'Sweet treats and desserts to satisfy your sweet tooth'
            },
            {
                'name': 'Appetizer',
                'slug': 'appetizer',
                'description': 'Starter dishes and snacks to whet your appetite'
            },
            {
                'name': 'Vegetarian',
                'slug': 'vegetarian',
                'description': 'Plant-based recipes for healthy and delicious meals'
            },
            {
                'name': 'Vegan',
                'slug': 'vegan',
                'description': 'Completely plant-based recipes without any animal products'
            },
            {
                'name': 'Quick & Easy',
                'slug': 'quick-easy',
                'description': 'Fast and simple recipes for busy weeknights'
            },
            {
                'name': 'Healthy',
                'slug': 'healthy',
                'description': 'Nutritious and wholesome recipes for a healthy lifestyle'
            },
            {
                'name': 'Comfort Food',
                'slug': 'comfort-food',
                'description': 'Hearty and satisfying dishes that warm the soul'
            },
            {
                'name': 'International',
                'slug': 'international',
                'description': 'Global cuisine and authentic recipes from around the world'
            },
            {
                'name': 'Holiday',
                'slug': 'holiday',
                'description': 'Special recipes for holidays and celebrations'
            }
        ]
        
        created_count = 0
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            if created:
                created_count += 1
                self.stdout.write(f'Created category: {category.name}')
            else:
                self.stdout.write(f'Category already exists: {category.name}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully processed {len(categories_data)} categories. Created {created_count} new categories.')
        )
