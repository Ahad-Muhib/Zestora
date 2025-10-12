"""
Integration test for the enhanced search functionality via web interface
"""

import requests
from django.test import TestCase, LiveServerTestCase
from django.contrib.auth.models import User
from recipes.models import Recipe, Category


class SearchIntegrationTest(LiveServerTestCase):
    """Test search functionality through the web interface"""
    
    def setUp(self):
        # Create test users
        self.chef = User.objects.create_user(
            username='testchef',
            email='chef@example.com',
            first_name='Test',
            last_name='Chef'
        )
        
        # Create test category
        self.category = Category.objects.create(
            name='Desserts',
            slug='desserts'
        )
        
        # Create test recipe
        self.recipe = Recipe.objects.create(
            title='Amazing Chocolate Cake',
            slug='amazing-chocolate-cake',
            description='Rich and delicious chocolate cake',
            ingredients='Chocolate, flour, eggs, sugar',
            instructions='Mix ingredients and bake',
            prep_time=20,
            cook_time=40,
            servings=8,
            difficulty='medium',
            category=self.category,
            author=self.chef
        )
    
    def test_search_by_recipe_title_via_web(self):
        """Test searching by recipe title through web interface"""
        response = self.client.get('/search/', {'q': 'chocolate'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Amazing Chocolate Cake')
        self.assertContains(response, 'Test Chef')
    
    def test_search_by_chef_name_via_web(self):
        """Test searching by chef name through web interface"""
        response = self.client.get('/search/', {'q': 'Test Chef'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Amazing Chocolate Cake')
        self.assertContains(response, 'Test Chef')
    
    def test_search_by_chef_username_via_web(self):
        """Test searching by chef username through web interface"""
        response = self.client.get('/search/', {'q': 'testchef'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Amazing Chocolate Cake')
        self.assertContains(response, 'Test Chef')
    
    def test_search_empty_query_via_web(self):
        """Test search with empty query"""
        response = self.client.get('/search/', {'q': ''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Start Your Search')
    
    def test_search_no_results_via_web(self):
        """Test search with no results"""
        response = self.client.get('/search/', {'q': 'nonexistentrecipe'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No recipes found matching')


class SearchViewTest(TestCase):
    """Test the search view functionality"""
    
    def setUp(self):
        # Create test users
        self.chef = User.objects.create_user(
            username='viewtestchef',
            email='viewchef@example.com',
            first_name='View',
            last_name='TestChef'
        )
        
        # Create test category
        self.category = Category.objects.create(
            name='Main Dishes',
            slug='main-dishes'
        )
        
        # Create test recipe
        self.recipe = Recipe.objects.create(
            title='Delicious Pasta',
            slug='delicious-pasta',
            description='Creamy pasta with vegetables',
            ingredients='Pasta, cream, vegetables',
            instructions='Cook pasta and add cream and vegetables',
            prep_time=15,
            cook_time=25,
            servings=4,
            difficulty='easy',
            category=self.category,
            author=self.chef
        )
    
    def test_search_context_includes_all_sections(self):
        """Test that search context includes recipes, tips, and stories"""
        response = self.client.get('/search/', {'q': 'pasta'})
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('recipes', response.context)
        self.assertIn('tips', response.context)
        self.assertIn('stories', response.context)
        self.assertIn('query', response.context)
        self.assertEqual(response.context['query'], 'pasta')
    
    def test_search_template_displays_chef_name(self):
        """Test that search results template displays chef names"""
        response = self.client.get('/search/', {'q': 'pasta'})
        
        self.assertEqual(response.status_code, 200)
        # Check that the chef's full name is displayed
        self.assertContains(response, 'View TestChef')
        # Check that the recipe is found
        self.assertContains(response, 'Delicious Pasta')
    
    def test_search_results_distinct(self):
        """Test that search results are distinct"""
        response = self.client.get('/search/', {'q': 'View'})
        
        self.assertEqual(response.status_code, 200)
        recipes = response.context['recipes']
        
        # Should only have one instance of each recipe
        recipe_ids = [recipe.id for recipe in recipes]
        unique_recipe_ids = set(recipe_ids)
        self.assertEqual(len(recipe_ids), len(unique_recipe_ids))