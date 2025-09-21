#!/usr/bin/env python
"""
Script to help organize recipe images for Zestora
This script will help you rename your recipe images to match the recipe slugs
"""

import os
import shutil
from pathlib import Path

def organize_images():
    print("🍽️  Zestora Recipe Image Organizer")
    print("=" * 50)
    
    # Recipe mappings (slug: display_name)
    recipes = {
        'savory-herb-chicken': 'Savory Herb-Infused Chicken',
        'chocolate-mousse': 'Decadent Chocolate Mousse',
        'mediterranean-quinoa-bowl': 'Mediterranean Quinoa Bowl',
        'fluffy-pancakes-berries': 'Fluffy Pancakes with Berries',
        'creamy-mushroom-risotto': 'Creamy Mushroom Risotto',
        'avocado-toast-deluxe': 'Avocado Toast Deluxe'
    }
    
    print("Current recipes in the database:")
    for i, (slug, name) in enumerate(recipes.items(), 1):
        print(f"{i}. {name} (slug: {slug})")
    
    print("\n" + "=" * 50)
    print("📁 Instructions for organizing your images:")
    print("=" * 50)
    
    print("\n1. Create a folder called 'recipe_images' in your project directory")
    print("2. Add your recipe images to this folder")
    print("3. Rename your images to match the recipe slugs:")
    
    for slug, name in recipes.items():
        print(f"   - {slug}.jpg (for {name})")
    
    print("\n4. Supported image formats: .jpg, .jpeg, .png, .webp")
    print("5. Recommended image size: 800x600 pixels or larger")
    print("6. Make sure images are high quality and well-lit")
    
    print("\n" + "=" * 50)
    print("🚀 After organizing your images, run:")
    print("   python manage.py add_recipe_images")
    print("=" * 50)
    
    # Check if recipe_images directory exists
    if os.path.exists('recipe_images'):
        print(f"\n✅ Found 'recipe_images' directory!")
        print("📋 Images in the directory:")
        
        image_files = []
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.webp']:
            image_files.extend(Path('recipe_images').glob(ext))
        
        if image_files:
            for img in image_files:
                print(f"   - {img.name}")
        else:
            print("   (No image files found)")
    else:
        print(f"\n❌ 'recipe_images' directory not found")
        print("   Please create it and add your images")

if __name__ == '__main__':
    organize_images()
