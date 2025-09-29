from django.core.management.base import BaseCommand
from recipes.models import Recipe
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Map existing images to recipes and identify truly missing ones'

    def handle(self, *args, **options):
        # Available images in the static/images/recipes directory
        available_images = [
            'avocado-toast.jpg',
            'beef-tacos.jpg', 
            'blueberry-pancakes.jpg',
            'caesar-salad.jpg',
            'chocolate-mousse.jpg',
            'french-toast.jpg',
            'grilled-sandwich.jpg',
            'herb-chicken.jpg',
            'pasta-salad.jpg',
            'quinoa-bowl.jpg',
            'salmon-teriyaki.jpg',
            'thai-curry.jpg',
            'tiramisu.jpg',
            'veggie-stir-fry.jpg'
        ]
        
        # Improved mapping using semantic matching
        image_mapping = {
            'savory-herb-chicken': 'herb-chicken.jpg',
            'chocolate-mousse': 'chocolate-mousse.jpg', 
            'mediterranean-quinoa-bowl': 'quinoa-bowl.jpg',
            'fluffy-pancakes-berries': 'blueberry-pancakes.jpg',
            'creamy-mushroom-risotto': 'pasta-salad.jpg',  # closest match
            'avocado-toast-deluxe': 'avocado-toast.jpg',
            'classic-pancakes': 'french-toast.jpg',  # similar breakfast item
            'grilled-chicken-caesar-salad': 'caesar-salad.jpg',
            'spaghetti-carbonara': 'pasta-salad.jpg',
            'chocolate-chip-cookies': 'tiramisu.jpg',  # closest dessert
            'stuffed-mushrooms': 'veggie-stir-fry.jpg',  # closest vegetable dish
            'quinoa-buddha-bowl': 'quinoa-bowl.jpg',
        }
        
        updated_count = 0
        missing_images = []
        
        self.stdout.write("=== RECIPE IMAGE MAPPING ANALYSIS ===\n")
        
        for recipe in Recipe.objects.all():
            if recipe.slug in image_mapping:
                image_file = image_mapping[recipe.slug]
                image_path = f'recipes/{image_file}'
                
                # Check if the image file exists
                static_image_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'recipes', image_file)
                if os.path.exists(static_image_path):
                    # Update the recipe only if it doesn't already have this image
                    if recipe.image != image_path:
                        recipe.image = image_path
                        recipe.save()
                        updated_count += 1
                        self.stdout.write(f'✓ Updated: "{recipe.title}" → {image_file}')
                    else:
                        self.stdout.write(f'✓ Already mapped: "{recipe.title}" → {image_file}')
                else:
                    self.stdout.write(f'✗ Image missing: {image_file} for "{recipe.title}"')
                    missing_images.append((recipe.slug, recipe.title, image_file))
            else:
                # Check if exact slug match exists
                exact_match = f'{recipe.slug}.jpg'
                if exact_match in available_images:
                    recipe.image = f'recipes/{exact_match}'
                    recipe.save()
                    updated_count += 1
                    self.stdout.write(f'✓ Exact match: "{recipe.title}" → {exact_match}')
                else:
                    missing_images.append((recipe.slug, recipe.title, f'{recipe.slug}.jpg'))
        
        self.stdout.write(f'\n=== SUMMARY ===')
        self.stdout.write(f'Updated {updated_count} recipe image mappings')
        
        if missing_images:
            self.stdout.write(f'\n=== TRULY MISSING IMAGES ===')
            self.stdout.write('The following images need to be uploaded to static/images/recipes/:')
            for slug, title, suggested_filename in missing_images:
                self.stdout.write(f'- {suggested_filename} (for "{title}")')
        else:
            self.stdout.write('\n🎉 All recipes now have images mapped!')
            
        # Show available unused images
        used_images = set()
        for recipe in Recipe.objects.all():
            if recipe.image:
                filename = recipe.image.name.split('/')[-1]
                used_images.add(filename)
        
        unused_images = set(available_images) - used_images
        if unused_images:
            self.stdout.write(f'\n=== UNUSED IMAGES ===')
            self.stdout.write('These images are available but not currently mapped:')
            for img in sorted(unused_images):
                self.stdout.write(f'- {img}')