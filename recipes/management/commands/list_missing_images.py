from django.core.management.base import BaseCommand
from recipes.models import Recipe
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'List missing recipe images'

    def handle(self, *args, **options):
        recipes = Recipe.objects.all()
        missing_images = []
        
        for recipe in recipes:
            expected_image_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'recipes', f'{recipe.slug}.jpg')
            if not os.path.exists(expected_image_path):
                missing_images.append((recipe.slug, recipe.title))
        
        if missing_images:
            self.stdout.write("Missing recipe images that need to be uploaded:")
            for slug, title in missing_images:
                self.stdout.write(f"- {slug}.jpg (for \"{title}\")")
        else:
            self.stdout.write("All recipes have matching image files!")