from django.core.management.base import BaseCommand
from django.core.files import File
from recipes.models import Recipe
import os
from pathlib import Path

class Command(BaseCommand):
    help = 'Add images to existing recipes from a specified directory'

    def add_arguments(self, parser):
        parser.add_argument(
            '--image-dir',
            type=str,
            help='Directory containing recipe images',
            default='recipe_images'
        )

    def handle(self, *args, **options):
        image_dir = options['image_dir']
        
        if not os.path.exists(image_dir):
            self.stdout.write(
                self.style.ERROR(f'Image directory "{image_dir}" does not exist.')
            )
            self.stdout.write(
                'Please create the directory and add your recipe images with descriptive names like:'
            )
            self.stdout.write('- savory-herb-chicken.jpg')
            self.stdout.write('- chocolate-mousse.jpg')
            self.stdout.write('- mediterranean-quinoa-bowl.jpg')
            self.stdout.write('- fluffy-pancakes-berries.jpg')
            self.stdout.write('- creamy-mushroom-risotto.jpg')
            self.stdout.write('- avocado-toast-deluxe.jpg')
            return

        # Get all recipes
        recipes = Recipe.objects.all()
        
        if not recipes.exists():
            self.stdout.write(
                self.style.ERROR('No recipes found. Please add some recipes first.')
            )
            return

        self.stdout.write(f'Found {recipes.count()} recipes to process...')
        
        # Process each recipe
        updated_count = 0
        for recipe in recipes:
            # Look for image files that match the recipe slug
            possible_names = [
                f'{recipe.slug}.jpg',
                f'{recipe.slug}.jpeg',
                f'{recipe.slug}.png',
                f'{recipe.slug}.webp',
                f'{recipe.title.lower().replace(" ", "-")}.jpg',
                f'{recipe.title.lower().replace(" ", "-")}.jpeg',
                f'{recipe.title.lower().replace(" ", "-")}.png',
                f'{recipe.title.lower().replace(" ", "-")}.webp',
            ]
            
            image_found = False
            for image_name in possible_names:
                image_path = os.path.join(image_dir, image_name)
                if os.path.exists(image_path):
                    # Add the image to the recipe
                    with open(image_path, 'rb') as f:
                        django_file = File(f)
                        recipe.image.save(image_name, django_file, save=True)
                    
                    self.stdout.write(f'Added image to: {recipe.title}')
                    updated_count += 1
                    image_found = True
                    break
            
            if not image_found:
                self.stdout.write(f'No image found for: {recipe.title}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated_count} recipes with images.')
        )
        
        if updated_count < recipes.count():
            self.stdout.write(
                self.style.WARNING(
                    f'{recipes.count() - updated_count} recipes still need images.'
                )
            )
