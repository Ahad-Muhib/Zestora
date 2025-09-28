import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File
from recipes.models import Recipe

class Command(BaseCommand):
    help = 'Migrate existing static image paths to ImageField'
    
    def handle(self, *args, **options):
        # Get recipes that don't have images but should have them based on static files
        recipes_without_images = Recipe.objects.filter(image__isnull=True)
        
        migrated_count = 0
        for recipe in recipes_without_images:
            # Check if there's a corresponding static image file
            static_image_path = f'images/recipes/{recipe.slug}.jpg'
            full_static_path = os.path.join(settings.BASE_DIR, 'static', static_image_path)
            
            if os.path.exists(full_static_path):
                try:
                    # Create media directory if it doesn't exist
                    media_recipes_dir = os.path.join(settings.MEDIA_ROOT, 'recipes')
                    os.makedirs(media_recipes_dir, exist_ok=True)
                    
                    # Copy the static image to media directory
                    media_filename = f'{recipe.slug}.jpg'
                    media_path = os.path.join(media_recipes_dir, media_filename)
                    
                    # Copy file to media directory
                    shutil.copy2(full_static_path, media_path)
                    
                    # Update the recipe's image field
                    with open(media_path, 'rb') as f:
                        recipe.image.save(media_filename, File(f), save=True)
                    
                    migrated_count += 1
                    self.stdout.write(f"Migrated: {recipe.title} -> {media_filename}")
                    
                except Exception as e:
                    self.stdout.write(f"Error migrating {recipe.title}: {str(e)}")
            else:
                # Try alternative naming patterns
                alt_patterns = [
                    f'images/recipes/{recipe.title.lower().replace(" ", "-")}.jpg',
                    f'images/recipes/{recipe.title.lower().replace(" ", "_")}.jpg',
                ]
                
                for pattern in alt_patterns:
                    alt_path = os.path.join(settings.BASE_DIR, 'static', pattern)
                    if os.path.exists(alt_path):
                        try:
                            media_recipes_dir = os.path.join(settings.MEDIA_ROOT, 'recipes')
                            os.makedirs(media_recipes_dir, exist_ok=True)
                            
                            media_filename = f'{recipe.slug}.jpg'
                            media_path = os.path.join(media_recipes_dir, media_filename)
                            
                            shutil.copy2(alt_path, media_path)
                            
                            with open(media_path, 'rb') as f:
                                recipe.image.save(media_filename, File(f), save=True)
                            
                            migrated_count += 1
                            self.stdout.write(f"Migrated (alt pattern): {recipe.title} -> {media_filename}")
                            break
                            
                        except Exception as e:
                            self.stdout.write(f"Error migrating {recipe.title}: {str(e)}")
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully migrated {migrated_count} recipe images!')
        )