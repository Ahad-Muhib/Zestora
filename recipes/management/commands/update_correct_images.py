from django.core.management.base import BaseCommand
from recipes.models import Recipe

class Command(BaseCommand):
    help = 'Update recipe images to use correct specific images'

    def handle(self, *args, **options):
        # Correct image mappings for the problematic recipes
        correct_mappings = {
            'creamy-mushroom-risotto': 'recipes/creamy-mushroom-risotto.jpg',
            'classic-pancakes': 'recipes/classic-pancakes.jpg', 
            'spaghetti-carbonara': 'recipes/spaghetti-carbonara.jpg',
            'chocolate-chip-cookies': 'recipes/chocolate-chip-cookies.jpg',
            'stuffed-mushrooms': 'recipes/stuffed-mushrooms.jpg',
            'quinoa-buddha-bowl': 'recipes/quinoa-buddha-bowl.jpg',
        }
        
        updated_count = 0
        
        for recipe in Recipe.objects.all():
            if recipe.slug in correct_mappings:
                new_image_path = correct_mappings[recipe.slug]
                if recipe.image != new_image_path:
                    recipe.image = new_image_path
                    recipe.save()
                    updated_count += 1
                    self.stdout.write(f'✓ Updated: "{recipe.title}" → {new_image_path}')
                else:
                    self.stdout.write(f'- Already correct: "{recipe.title}"')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated_count} recipe images!')
        )