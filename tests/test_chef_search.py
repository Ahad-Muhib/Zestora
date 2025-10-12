"""
Test the enhanced search functionality for chef names
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models import Q
from recipes.models import Recipe, Category
from userprofile.models import UserProfile


class ChefSearchTests(TestCase):
    """Test searching recipes by chef names"""
    
    def setUp(self):
        # Create test users
        self.chef1 = User.objects.create_user(
            username='johndoe',
            email='john@example.com',
            first_name='John',
            last_name='Doe'
        )
        
        self.chef2 = User.objects.create_user(
            username='mariagarcia',
            email='maria@example.com',
            first_name='Maria',
            last_name='Garcia'
        )
        
        self.chef3 = User.objects.create_user(
            username='alexsmith',
            email='alex@example.com',
            first_name='Alex',
            last_name='Smith'
        )
        
        # Create test category
        self.category = Category.objects.create(
            name='Main Course',
            slug='main-course'
        )
        
        # Create test recipes
        self.recipe1 = Recipe.objects.create(
            title='John\'s Famous Pasta',
            slug='johns-famous-pasta',
            description='A delicious pasta recipe',
            ingredients='Pasta, tomato sauce, cheese',
            instructions='Cook pasta and add sauce',
            prep_time=15,
            cook_time=20,
            servings=4,
            difficulty='easy',
            category=self.category,
            author=self.chef1
        )
        
        self.recipe2 = Recipe.objects.create(
            title='Traditional Tacos',
            slug='traditional-tacos',
            description='Authentic Mexican tacos',
            ingredients='Tortillas, beef, onions, cilantro',
            instructions='Cook beef and assemble tacos',
            prep_time=10,
            cook_time=15,
            servings=6,
            difficulty='medium',
            category=self.category,
            author=self.chef2
        )
        
        self.recipe3 = Recipe.objects.create(
            title='Quick Salad',
            slug='quick-salad',
            description='Fresh garden salad',
            ingredients='Lettuce, tomatoes, cucumber',
            instructions='Mix all ingredients',
            prep_time=5,
            cook_time=0,
            servings=2,
            difficulty='easy',
            category=self.category,
            author=self.chef3
        )
    
    def get_search_results(self, query):
        """Get search results using the enhanced search query"""
        return Recipe.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) | 
            Q(ingredients__icontains=query) |
            Q(author__username__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query)
        ).select_related('author', 'category').distinct()
    
    def test_search_by_username(self):
        """Test searching recipes by chef username"""
        results = self.get_search_results('johndoe')
        self.assertEqual(results.count(), 1)
        self.assertIn(self.recipe1, results)
        
        results = self.get_search_results('maria')
        self.assertEqual(results.count(), 1)
        self.assertIn(self.recipe2, results)
    
    def test_search_by_first_name(self):
        """Test searching recipes by chef first name"""
        results = self.get_search_results('John')
        self.assertEqual(results.count(), 1)
        self.assertIn(self.recipe1, results)
        
        results = self.get_search_results('Maria')
        self.assertEqual(results.count(), 1)
        self.assertIn(self.recipe2, results)
    
    def test_search_by_last_name(self):
        """Test searching recipes by chef last name"""
        results = self.get_search_results('Doe')
        self.assertEqual(results.count(), 1)
        self.assertIn(self.recipe1, results)
        
        results = self.get_search_results('Garcia')
        self.assertEqual(results.count(), 1)
        self.assertIn(self.recipe2, results)
    
    def test_search_chef_name_case_insensitive(self):
        """Test that chef name search is case insensitive"""
        results = self.get_search_results('JOHN')
        self.assertEqual(results.count(), 1)
        self.assertIn(self.recipe1, results)
        
        results = self.get_search_results('garcia')
        self.assertEqual(results.count(), 1)
        self.assertIn(self.recipe2, results)
    
    def test_search_partial_chef_name(self):
        """Test searching with partial chef names"""
        results = self.get_search_results('Jo')
        self.assertEqual(results.count(), 1)
        self.assertIn(self.recipe1, results)
        
        results = self.get_search_results('Alex')
        self.assertEqual(results.count(), 1)
        self.assertIn(self.recipe3, results)
    
    def test_search_combined_recipe_and_chef(self):
        """Test that search still works for recipe content when chef name is in query"""
        # Search for 'pasta' - should find recipe by title
        results = self.get_search_results('pasta')
        self.assertEqual(results.count(), 1)
        self.assertIn(self.recipe1, results)
        
        # Search for 'Mexican' - should find recipe by description
        results = self.get_search_results('Mexican')
        self.assertEqual(results.count(), 1)
        self.assertIn(self.recipe2, results)
    
    def test_search_no_results_for_nonexistent_chef(self):
        """Test search with non-existent chef name returns no results"""
        results = self.get_search_results('nonexistentchef')
        self.assertEqual(results.count(), 0)
    
    def test_search_chef_with_common_name_in_recipe(self):
        """Test edge case where chef name appears in recipe content"""
        # Create a recipe that mentions 'John' in the description
        recipe4 = Recipe.objects.create(
            title='Uncle John\'s Secret Recipe',
            slug='uncle-johns-secret-recipe',
            description='A recipe passed down from Uncle John',
            ingredients='Special ingredients',
            instructions='Follow John\'s method',
            prep_time=30,
            cook_time=45,
            servings=8,
            difficulty='hard',
            category=self.category,
            author=self.chef3  # Note: authored by Alex, not John
        )
        
        # Search for 'John' should return both John's recipe and the recipe mentioning John
        results = self.get_search_results('John')
        self.assertEqual(results.count(), 2)
        self.assertIn(self.recipe1, results)  # John's actual recipe
        self.assertIn(recipe4, results)       # Recipe mentioning John
    
    def test_search_distinct_results(self):
        """Test that search returns distinct results without duplicates"""
        # Create a scenario that could potentially return duplicates
        # if distinct() wasn't used properly
        results = self.get_search_results('John')
        
        # Convert to list to check for actual duplicates
        results_list = list(results)
        unique_ids = set(recipe.id for recipe in results_list)
        
        # Should have same number of unique IDs as total results
        self.assertEqual(len(results_list), len(unique_ids))
    
    def test_user_profile_full_name_property(self):
        """Test that user profile full_name property works correctly"""
        # Test user with both first and last name
        self.assertEqual(self.chef1.profile.full_name, 'John Doe')
        
        # Test user with only username (no first/last name)
        chef_no_name = User.objects.create_user(
            username='chef_username_only',
            email='chef@example.com'
        )
        self.assertEqual(chef_no_name.profile.full_name, 'chef_username_only')
        
        # Test user with only first name
        chef_first_only = User.objects.create_user(
            username='chef_first',
            email='first@example.com',
            first_name='First'
        )
        self.assertEqual(chef_first_only.profile.full_name, 'First')