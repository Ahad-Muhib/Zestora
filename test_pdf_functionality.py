#!/usr/bin/env python
"""
Test script to verify PDF generation functionality
"""
import os
import django
import requests

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zestora.settings')
django.setup()

from recipes.models import Recipe

def test_pdf_generation():
    """Test PDF generation for all recipes"""
    print("🧪 Testing PDF generation functionality...")
    
    recipes = Recipe.objects.all()
    print(f"📋 Found {recipes.count()} recipes to test")
    
    base_url = "http://127.0.0.1:8001"
    
    for recipe in recipes[:3]:  # Test first 3 recipes
        print(f"\n🍽️  Testing recipe: {recipe.title}")
        print(f"   Slug: {recipe.slug}")
        
        # Test recipe detail page
        detail_url = f"{base_url}/recipes/{recipe.slug}/"
        try:
            response = requests.get(detail_url, timeout=10)
            if response.status_code == 200:
                print(f"   ✅ Recipe detail page: OK (200)")
            else:
                print(f"   ❌ Recipe detail page: {response.status_code}")
        except requests.RequestException as e:
            print(f"   ❌ Recipe detail page error: {e}")
        
        # Test PDF download
        pdf_url = f"{base_url}/recipes/{recipe.slug}/pdf/"
        try:
            response = requests.get(pdf_url, timeout=15)
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                content_length = len(response.content)
                print(f"   ✅ PDF download: OK (200)")
                print(f"   📄 Content-Type: {content_type}")
                print(f"   📊 Size: {content_length:,} bytes")
                
                # Verify it's actually a PDF
                if response.content.startswith(b'%PDF'):
                    print(f"   ✅ Valid PDF format")
                else:
                    print(f"   ⚠️  Response doesn't appear to be a PDF")
            else:
                print(f"   ❌ PDF download: {response.status_code}")
        except requests.RequestException as e:
            print(f"   ❌ PDF download error: {e}")
    
    print(f"\n🎉 PDF functionality testing complete!")

if __name__ == "__main__":
    test_pdf_generation()