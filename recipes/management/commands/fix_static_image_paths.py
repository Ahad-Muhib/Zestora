from django.core.management.base import BaseCommand
from recipes.models import Recipe

class Command(BaseCommand):
    help = 'Update recipe image paths to use static paths'

    def handle(self, *args, **options):
        # Update all recipes to use static image paths
        image_mappings = {
            'savory-herb-chicken': 'images/recipes/herb-chicken.jpg',
            'chocolate-mousse': 'images/recipes/chocolate-mousse.jpg',
            'mediterranean-quinoa-bowl': 'images/recipes/quinoa-bowl.jpg',
            'fluffy-pancakes-berries': 'images/recipes/blueberry-pancakes.jpg',
            'creamy-mushroom-risotto': 'images/recipes/creamy-mushroom-risotto.jpg',
            'avocado-toast-deluxe': 'images/recipes/avocado-toast.jpg',
            'classic-pancakes': 'images/recipes/classic-pancakes.jpg',
            'grilled-chicken-caesar-salad': 'images/recipes/caesar-salad.jpg',
            'spaghetti-carbonara': 'images/recipes/spaghetti-carbonara.jpg',
            'chocolate-chip-cookies': 'images/recipes/chocolate-chip-cookies.jpg',
            'stuffed-mushrooms': 'images/recipes/stuffed-mushrooms.jpg',
            'quinoa-buddha-bowl': 'images/recipes/quinoa-buddha-bowl.jpg',
        }
        
        updated_count = 0
        
        for recipe in Recipe.objects.all():
            if recipe.slug in image_mappings:
                new_image_path = image_mappings[recipe.slug]
                recipe.image = new_image_path
                recipe.save()
                updated_count += 1
                self.stdout.write(f'✓ Updated: "{recipe.title}" → {new_image_path}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated_count} recipe image paths to static!')
        )