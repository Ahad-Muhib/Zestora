from django.core.management.base import BaseCommand
from recipes.models import Recipe
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Link existing recipe images to recipes in database'

    def handle(self, *args, **options):
        # Image mapping based on recipe slugs and available image files
        image_mapping = {
            'savory-herb-chicken': 'herb-chicken.jpg',
            'chocolate-mousse': 'chocolate-mousse.jpg', 
            'mediterranean-quinoa-bowl': 'quinoa-bowl.jpg',
            'fluffy-pancakes-berries': 'blueberry-pancakes.jpg',
            'creamy-mushroom-risotto': 'pasta-salad.jpg',  # placeholder
            'avocado-toast-deluxe': 'avocado-toast.jpg',
            'classic-pancakes': 'french-toast.jpg',
            'grilled-chicken-caesar-salad': 'caesar-salad.jpg',
            'spaghetti-carbonara': 'pasta-salad.jpg',
            'chocolate-chip-cookies': 'tiramisu.jpg',  # placeholder 
            'stuffed-mushrooms': 'veggie-stir-fry.jpg',  # placeholder
            'quinoa-buddha-bowl': 'quinoa-bowl.jpg',
        }
        
        updated_count = 0
        
        for recipe in Recipe.objects.all():
            if recipe.slug in image_mapping:
                image_file = image_mapping[recipe.slug]
                image_path = f'recipes/{image_file}'
                
                # Check if the image file exists
                static_image_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'recipes', image_file)
                if os.path.exists(static_image_path):
                    recipe.image = image_path
                    recipe.save()
                    updated_count += 1
                    self.stdout.write(f'✓ Linked {recipe.title} to {image_file}')
                else:
                    self.stdout.write(f'✗ Image {image_file} not found for {recipe.title}')
            else:
                self.stdout.write(f'- No image mapping for {recipe.title} ({recipe.slug})')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully linked {updated_count} recipe images!')
        )