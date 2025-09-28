import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zestora.settings')
django.setup()

from recipes.models import Recipe

# Check the most recently created recipes to see their image paths
recent_recipes = Recipe.objects.order_by('-created_at')[:5]
print("Recent recipes and their image paths:")
for recipe in recent_recipes:
    print(f"Recipe: {recipe.title}")
    print(f"  Created: {recipe.created_at}")
    print(f"  Image path: {recipe.image.name if recipe.image else 'None'}")
    if recipe.image:
        print(f"  First 8 chars: '{recipe.image.name[:8]}'")
        print(f"  Starts with 'recipes/': {recipe.image.name.startswith('recipes/')}")
    print("---")