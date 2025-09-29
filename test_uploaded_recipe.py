import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zestora.settings')
django.setup()

from recipes.models import Recipe, Category
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

# Create a test recipe with uploaded image (simulating form upload)
user = User.objects.first()
category = Category.objects.first()

# Simulate an uploaded image file
test_image_content = b"fake image content"
uploaded_file = SimpleUploadedFile(
    name="test-uploaded-image.jpg",
    content=test_image_content,
    content_type="image/jpeg"
)

test_recipe = Recipe.objects.create(
    title='Test Form Upload Recipe',
    slug='test-form-upload-recipe',
    description='Testing form upload behavior',
    ingredients='Test ingredient 1\nTest ingredient 2',
    instructions='Step 1: Test\nStep 2: More test',
    prep_time=10,
    cook_time=15,
    servings=2,
    difficulty='easy',
    category=category,
    author=user,
    image=uploaded_file  # This simulates a form upload
)

print(f'Created test recipe: {test_recipe.title}')
print(f'Image path: {test_recipe.image.name}')
print(f'Image name length: {len(test_recipe.image.name)}')
print(f'First 8 chars: "{test_recipe.image.name[:8]}"')
print(f'Starts with "recipes/": {test_recipe.image.name.startswith("recipes/")}')

# Clean up - delete the test recipe
test_recipe.delete()
print('Test recipe deleted')