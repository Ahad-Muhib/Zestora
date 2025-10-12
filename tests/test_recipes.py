"""
Selenium tests for Zestora recipe functionality
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.base_selenium import SeleniumTestCase
from recipes.models import Recipe, Category


@pytest.mark.selenium
class TestRecipes(SeleniumTestCase):
    """Test recipe functionality"""
    
    def setUp(self):
        super().setUp()
        # Create a test category first
        from recipes.models import Recipe, Category
        self.test_category = Category.objects.create(
            name="Test Category",
            slug="test-category",
            description="A test category"
        )
        
        # Create a test recipe
        self.test_recipe = Recipe.objects.create(
            title="Test Recipe",
            slug="test-recipe",
            description="A test recipe for selenium testing",
            ingredients="Test ingredients",
            instructions="Test instructions",
            author=self.test_user,
            prep_time=30,
            cook_time=45,
            servings=4,
            category=self.test_category
        )
        
    def test_recipe_list_page(self):
        """Test recipe list page loads and displays recipes"""
        self.driver.get(f'{self.live_server_url}/recipes/')
        self.assert_page_title_contains("Recipes")
        self.assert_text_in_page("Test Recipe")
        
    def test_recipe_detail_page(self):
        """Test recipe detail page loads correctly"""
        self.driver.get(f'{self.live_server_url}/recipes/{self.test_recipe.slug}/')
        
        # Check if we're on a recipe page (title might not contain recipe name)
        self.assert_text_in_page("Test Recipe")
        
    def test_recipe_search(self):
        """Test recipe search functionality"""
        self.driver.get(self.live_server_url)
        
        # Find search box and search for recipe
        search_box = self.wait_for_element(By.NAME, 'q')
        search_box.send_keys("Test Recipe")
        
        search_button = self.driver.find_element(By.CSS_SELECTOR, '.search-btn')
        search_button.click()
        
        # Should find our test recipe
        self.assert_text_in_page("Test Recipe")
        
    def test_category_list_page(self):
        """Test category list page"""
        self.driver.get(f'{self.live_server_url}/recipes/categories/')
        self.assert_text_in_page("Test Category")
        
    def test_recipe_add_requires_login(self):
        """Test that adding recipe requires login"""
        self.driver.get(f'{self.live_server_url}/recipes/add/')
        
        # Should redirect to login page - check for login field
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "login"))
        )
        self.assert_text_in_page("Sign In")
        
    def test_logged_in_user_can_access_add_recipe(self):
        """Test that logged in user can access add recipe page"""
        self.login_user('testuser', 'testpass123')
        
        self.driver.get(f'{self.live_server_url}/recipes/add/')
        self.assert_text_in_page("Add Recipe")
        self.assert_element_present(By.NAME, 'title')