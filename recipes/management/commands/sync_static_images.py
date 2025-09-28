from django.core.management.base import BaseCommand
from django.conf import settings
from recipes.models import Recipe
import os
import glob

class Command(BaseCommand):
    help = 'Synchronize recipe database entries with static image files'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be updated without making changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))
        
        # Get the static images directory
        static_images_dir = os.path.join(settings.BASE_DIR, 'static', 'images', 'recipes')
        
        if not os.path.exists(static_images_dir):
            self.stdout.write(self.style.ERROR(f'Static images directory not found: {static_images_dir}'))
            return
        
        # Get all available image files
        image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.webp']
        available_images = []
        
        for ext in image_extensions:
            available_images.extend(glob.glob(os.path.join(static_images_dir, ext)))
        
        self.stdout.write(f'Found {len(available_images)} image files in static directory')
        
        # Get all recipes from database
        recipes = Recipe.objects.all()
        updated_count = 0
        
        for recipe in recipes:
            # Try to find a matching image for this recipe
            recipe_slug = recipe.slug
            current_image = recipe.image.name if recipe.image else ''
            
            self.stdout.write(f'\\nProcessing recipe: {recipe.title} (slug: {recipe_slug})')
            self.stdout.write(f'Current image: {current_image}')
            
            # Look for images that match the recipe slug or title
            matching_images = []
            
            for image_path in available_images:
                image_filename = os.path.basename(image_path).lower()
                image_name = os.path.splitext(image_filename)[0]
                
                # Check if image filename matches recipe slug
                if recipe_slug.lower() in image_name or image_name in recipe_slug.lower():
                    matching_images.append(image_path)
                    continue
                
                # Check if image filename matches recipe title words
                title_words = recipe.title.lower().replace('-', ' ').split()
                if any(word in image_name for word in title_words if len(word) > 3):
                    matching_images.append(image_path)
            
            if matching_images:
                # Use the first matching image
                best_match = matching_images[0]
                relative_path = os.path.relpath(best_match, settings.BASE_DIR).replace('\\\\', '/')
                
                self.stdout.write(f'Found matching image: {relative_path}')
                
                if not dry_run:
                    recipe.image = relative_path
                    recipe.save()
                    updated_count += 1
                    self.stdout.write(self.style.SUCCESS(f'Updated recipe image path'))
                else:
                    self.stdout.write(self.style.WARNING(f'Would update image path to: {relative_path}'))
                    updated_count += 1
            else:
                self.stdout.write(self.style.WARNING('No matching image found'))
        
        if dry_run:
            self.stdout.write(self.style.SUCCESS(f'\\nDry run complete. Would update {updated_count} recipes.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'\\nSuccessfully updated {updated_count} recipes with image paths.'))
            
        self.stdout.write('\\nAvailable images:')
        for img in available_images:
            filename = os.path.basename(img)
            self.stdout.write(f'  - {filename}')