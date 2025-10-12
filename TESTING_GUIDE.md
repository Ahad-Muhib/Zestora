# Zestora Testing Guide

## Overview
This guide provides comprehensive instructions for running and understanding the test suite for the Zestora Django application. The test suite includes 113 tests covering models, forms, views, and user interactions.

## Table of Contents
- [Quick Start](#quick-start)
- [Test Categories](#test-categories)
- [Running Tests](#running-tests)
- [Unit Tests](#unit-tests)
- [Integration Tests](#integration-tests)
- [Selenium Tests](#selenium-tests)
- [Test Configuration](#test-configuration)
- [Writing New Tests](#writing-new-tests)
- [Troubleshooting](#troubleshooting)

## Quick Start

### Prerequisites
```bash
# Ensure you're in the project directory
cd /home/muhib/muhib/project/Zestora

# Activate virtual environment (if using one)
source venv/bin/activate

# Install test dependencies
pip install pytest pytest-django selenium
```

### Run All Tests
```bash
# Basic test run
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/

# Verbose output with test names
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/ -v

# Quick summary
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/ -q
```

## Test Categories

### 1. Model Tests (25 tests)
**File**: `tests/test_models_comprehensive.py`
**Purpose**: Validate Django models, relationships, and constraints

```bash
# Run all model tests
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/test_models_comprehensive.py -v

# Run specific model test
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/test_models_comprehensive.py::RecipeModelTests::test_recipe_creation -v
```

### 2. Form Validation Tests (18 tests)
**File**: `tests/test_forms_validation.py`
**Purpose**: Test form validation, field requirements, and user input handling

```bash
# Run all form tests
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/test_forms_validation.py -v

# Run specific form validation
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/test_forms_validation.py::RecipeFormTests -v
```

### 3. User Profile Tests (9 tests)
**File**: `tests/test_user_profiles.py`
**Purpose**: Test user profile functionality and relationships

```bash
# Run profile tests
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/test_user_profiles.py -v
```

### 4. Recipe Advanced Tests (13 tests)
**File**: `tests/test_recipe_advanced.py`
**Purpose**: Test advanced recipe operations (CRUD, relationships, saved recipes)

```bash
# Run advanced recipe tests
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/test_recipe_advanced.py -v
```

### 5. Search Functionality Tests (10 tests)
**File**: `tests/test_search_functionality.py`
**Purpose**: Test search features, filtering, and result handling

```bash
# Run search tests
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/test_search_functionality.py -v
```

## Running Tests

### Basic Commands

```bash
# Run all tests
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/

# Run with coverage report
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/ --cov=.

# Run specific test file
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/test_models_comprehensive.py

# Run specific test class
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/test_models_comprehensive.py::RecipeModelTests

# Run specific test method
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/test_models_comprehensive.py::RecipeModelTests::test_recipe_creation
```

### Advanced Test Filtering

```bash
# Run only unit tests (exclude Selenium)
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/ -k "not selenium"

# Run only Selenium tests
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/ -k "selenium"

# Run tests matching pattern
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/ -k "recipe"

# Run tests with specific markers
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/ -m "selenium"
```

### Output Options

```bash
# Verbose output
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/ -v

# Quiet output (minimal)
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/ -q

# Show local variables on failure
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/ -l

# Stop on first failure
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/ -x

# Show slowest tests
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/ --durations=10
```

## Unit Tests

### Model Unit Tests Example

```python
# Example from test_models_comprehensive.py
from django.test import TestCase
from django.contrib.auth.models import User
from recipes.models import Recipe, Category

class RecipeModelTests(TestCase):
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Test Category',
            description='Test description'
        )

    def test_recipe_creation(self):
        """Test recipe creation with required fields"""
        recipe = Recipe.objects.create(
            title='Test Recipe',
            description='Test description',
            ingredients='Test ingredients',
            instructions='Test instructions',
            prep_time=10,
            cook_time=20,
            servings=4,
            difficulty='easy',
            category=self.category,
            author=self.user
        )
        
        self.assertEqual(recipe.title, 'Test Recipe')
        self.assertEqual(recipe.author, self.user)
        self.assertEqual(recipe.category, self.category)
        self.assertTrue(recipe.created_at)
```

### Form Unit Tests Example

```python
# Example from test_forms_validation.py
from django.test import TestCase
from recipes.forms import RecipeForm

class RecipeFormTests(TestCase):
    def test_recipe_form_valid_data(self):
        """Test recipe form with valid data"""
        form_data = {
            'title': 'Test Recipe',
            'description': 'Test description',
            'ingredients': 'Test ingredients',
            'instructions': 'Test instructions',
            'prep_time': 10,
            'cook_time': 20,
            'servings': 4,
            'difficulty': 'easy',
        }
        
        form = RecipeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_recipe_form_missing_required_fields(self):
        """Test recipe form with missing required fields"""
        form_data = {
            'title': '',  # Required field left empty
            'description': 'Test description',
        }
        
        form = RecipeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
```

### Running Unit Tests Only

```bash
# Run only model tests (fastest)
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/test_models_comprehensive.py tests/test_forms_validation.py -v

# Run unit tests excluding Selenium
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/ -k "not selenium" -v
```

## Integration Tests

### View Integration Tests Example

```python
# Example from test_recipes.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class RecipeViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_recipe_list_view(self):
        """Test recipe list view returns 200"""
        response = self.client.get(reverse('recipes:recipe_list'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_create_requires_login(self):
        """Test recipe creation requires authentication"""
        response = self.client.get(reverse('recipes:add_recipe'))
        self.assertRedirects(response, '/login/?next=/recipes/add/')

    def test_recipe_create_authenticated(self):
        """Test recipe creation when authenticated"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('recipes:add_recipe'))
        self.assertEqual(response.status_code, 200)
```

### Running Integration Tests

```bash
# Run view/integration tests
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/test_recipes.py tests/test_community.py -v

# Run authentication tests
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/test_authentication.py -v
```

## Selenium Tests

### Selenium Test Example

```python
# Example from test_user_profiles.py
from tests.base_selenium import SeleniumTestCase
from selenium.webdriver.common.by import By

class UserProfileSeleniumTests(SeleniumTestCase):
    def test_profile_page_access(self):
        """Test accessing user profile page"""
        # Create and login user
        self.create_user("testuser", "testpass123")
        self.login_user("testuser", "testpass123")
        
        # Navigate to profile
        self.driver.get(f"{self.live_server_url}/profile/")
        
        # Verify profile content
        self.assertIn("testuser's Profile", self.driver.title)
        self.assertIn("testuser", self.driver.page_source)

    def test_profile_edit_form(self):
        """Test profile editing functionality"""
        self.create_user("testuser", "testpass123")
        self.login_user("testuser", "testpass123")
        
        # Navigate to edit page
        self.driver.get(f"{self.live_server_url}/profile/edit/")
        
        # Fill and submit form
        bio_field = self.driver.find_element(By.NAME, "bio")
        bio_field.clear()
        bio_field.send_keys("Updated bio text")
        
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Verify update
        self.assertIn("Updated bio text", self.driver.page_source)
```

### Running Selenium Tests

```bash
# Run all Selenium tests (requires Firefox)
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/ -k "selenium" -v

# Run specific Selenium test file
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/test_user_profiles.py -k "selenium" -v

# Run Selenium tests with browser visible (for debugging)
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/ -k "selenium" -s
```

## Test Configuration

### pytest.ini Configuration
```ini
# pytest.ini
[tool:pytest]
DJANGO_SETTINGS_MODULE = zestora.settings
python_files = tests.py test_*.py *_tests.py
addopts = --tb=short --strict-markers
markers =
    selenium: marks tests as selenium tests (deselect with '-m "not selenium"')
    slow: marks tests as slow (deselect with '-m "not slow"')
```

### Base Test Classes

#### Django Test Base
```python
# tests/base_test.py
from django.test import TestCase
from django.contrib.auth.models import User

class BaseTestCase(TestCase):
    def setUp(self):
        """Common setup for all tests"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def create_test_recipe(self):
        """Helper method to create test recipe"""
        from recipes.models import Recipe, Category
        category = Category.objects.create(name='Test Category')
        return Recipe.objects.create(
            title='Test Recipe',
            description='Test description',
            ingredients='Test ingredients',
            instructions='Test instructions',
            prep_time=10,
            cook_time=20,
            servings=4,
            difficulty='easy',
            category=category,
            author=self.user
        )
```

#### Selenium Test Base
```python
# tests/base_selenium.py
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

class SeleniumTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.add_argument('--headless')  # Run in background
        cls.driver = webdriver.Firefox(options=options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def create_user(self, username, password):
        """Helper to create test user"""
        from django.contrib.auth.models import User
        return User.objects.create_user(username=username, password=password)

    def login_user(self, username, password):
        """Helper to login user via Selenium"""
        self.driver.get(f"{self.live_server_url}/login/")
        self.driver.find_element("name", "username").send_keys(username)
        self.driver.find_element("name", "password").send_keys(password)
        self.driver.find_element("css selector", "button[type='submit']").click()
```

## Writing New Tests

### 1. Model Tests

```python
# tests/test_new_feature.py
from django.test import TestCase
from django.contrib.auth.models import User
from myapp.models import MyModel

class MyModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_model_creation(self):
        """Test creating a new model instance"""
        instance = MyModel.objects.create(
            name='Test Name',
            user=self.user
        )
        self.assertEqual(instance.name, 'Test Name')
        self.assertEqual(instance.user, self.user)

    def test_model_str_method(self):
        """Test string representation"""
        instance = MyModel.objects.create(
            name='Test Name',
            user=self.user
        )
        self.assertEqual(str(instance), 'Test Name')

    def test_model_validation(self):
        """Test model field validation"""
        with self.assertRaises(ValueError):
            MyModel.objects.create(
                name='',  # Invalid empty name
                user=self.user
            )
```

### 2. Form Tests

```python
from django.test import TestCase
from myapp.forms import MyForm

class MyFormTests(TestCase):
    def test_form_valid_data(self):
        """Test form with valid data"""
        form_data = {
            'field1': 'valid_value',
            'field2': 'another_valid_value',
        }
        form = MyForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        """Test form with invalid data"""
        form_data = {
            'field1': '',  # Required field left empty
        }
        form = MyForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('field1', form.errors)

    def test_form_save(self):
        """Test form save functionality"""
        form_data = {
            'field1': 'valid_value',
            'field2': 'another_valid_value',
        }
        form = MyForm(data=form_data)
        if form.is_valid():
            instance = form.save()
            self.assertEqual(instance.field1, 'valid_value')
```

### 3. View Tests

```python
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class MyViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_view_get(self):
        """Test GET request to view"""
        response = self.client.get(reverse('myapp:my_view'))
        self.assertEqual(response.status_code, 200)

    def test_view_post_authenticated(self):
        """Test POST request when authenticated"""
        self.client.login(username='testuser', password='testpass123')
        
        post_data = {
            'field1': 'value1',
            'field2': 'value2',
        }
        
        response = self.client.post(reverse('myapp:my_view'), post_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success

    def test_view_requires_login(self):
        """Test view requires authentication"""
        response = self.client.get(reverse('myapp:protected_view'))
        self.assertRedirects(response, '/login/?next=/protected/')
```

### 4. Selenium Tests

```python
from tests.base_selenium import SeleniumTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class MySeleniumTests(SeleniumTestCase):
    def test_user_interaction(self):
        """Test user interaction with the interface"""
        # Create and login user
        self.create_user("testuser", "testpass123")
        self.login_user("testuser", "testpass123")
        
        # Navigate to page
        self.driver.get(f"{self.live_server_url}/my-page/")
        
        # Find and interact with elements
        input_field = self.driver.find_element(By.NAME, "search")
        input_field.send_keys("test query")
        input_field.send_keys(Keys.RETURN)
        
        # Verify results
        self.assertIn("Search Results", self.driver.title)
        results = self.driver.find_elements(By.CLASS_NAME, "result-item")
        self.assertGreater(len(results), 0)

    def test_form_submission(self):
        """Test form submission via browser"""
        self.create_user("testuser", "testpass123")
        self.login_user("testuser", "testpass123")
        
        self.driver.get(f"{self.live_server_url}/form-page/")
        
        # Fill form
        self.driver.find_element(By.NAME, "title").send_keys("Test Title")
        self.driver.find_element(By.NAME, "description").send_keys("Test Description")
        
        # Submit
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        # Verify success
        self.assertIn("Success", self.driver.page_source)
```

## Test Database Management

### Automatic Database Handling
```bash
# Django automatically creates/destroys test databases
# No manual database setup needed

# To use a specific test database
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/ --reuse-db

# To keep test database for debugging
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/ --create-db --keep-db
```

### Test Data Fixtures
```python
# Using fixtures for consistent test data
from django.test import TestCase
from django.core.management import call_command

class MyTestsWithFixtures(TestCase):
    fixtures = ['test_users.json', 'test_recipes.json']
    
    def test_with_fixture_data(self):
        """Test using pre-loaded fixture data"""
        from django.contrib.auth.models import User
        user = User.objects.get(username='fixture_user')
        self.assertTrue(user.is_active)
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Django Settings Not Configured
```bash
# Error: django.core.exceptions.ImproperlyConfigured
# Solution: Always use DJANGO_SETTINGS_MODULE
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/
```

#### 2. Firefox Not Found (Selenium)
```bash
# Error: selenium.common.exceptions.WebDriverException
# Solution: Install Firefox or use Chrome driver
sudo apt-get install firefox  # Ubuntu/Debian
brew install firefox          # macOS
```

#### 3. Database Permission Errors
```bash
# Error: django.db.utils.OperationalError
# Solution: Ensure proper database permissions
# Test databases are created automatically with appropriate permissions
```

#### 4. Import Errors
```bash
# Error: ModuleNotFoundError
# Solution: Ensure you're in the correct directory
cd /home/muhib/muhib/project/Zestora
# And virtual environment is activated
source venv/bin/activate
```

#### 5. Test Isolation Issues
```python
# Problem: Tests affecting each other
# Solution: Use proper setUp/tearDown methods
class MyTests(TestCase):
    def setUp(self):
        """Reset state before each test"""
        # Create clean test data
        pass
    
    def tearDown(self):
        """Clean up after each test"""
        # Clean up if needed (usually automatic)
        pass
```

### Debug Failing Tests

```bash
# Run single failing test with verbose output
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/test_file.py::TestClass::test_method -v -s

# Run with debugger
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/test_file.py::TestClass::test_method --pdb

# Show local variables on failure
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/test_file.py -l

# Capture stdout (print statements)
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/test_file.py -s
```

### Performance Testing

```bash
# Show slowest tests
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/ --durations=10

# Profile test execution
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/ --profile

# Run tests in parallel (install pytest-xdist)
pip install pytest-xdist
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/ -n auto
```

## Test Coverage

### Generate Coverage Report
```bash
# Install coverage
pip install coverage pytest-cov

# Run tests with coverage
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/ --cov=. --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### Coverage Configuration
```ini
# .coveragerc
[run]
source = .
omit = 
    */venv/*
    */migrations/*
    manage.py
    */settings/*
    */tests/*
    */env/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
```

## Continuous Integration

### GitHub Actions Example
```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-django pytest-cov
    
    - name: Run tests
      run: |
        DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/ --cov=.
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v1
```

## Best Practices

### 1. Test Organization
- Keep tests in separate files by functionality
- Use descriptive test method names
- Group related tests in test classes
- Use setUp/tearDown for common test data

### 2. Test Data
- Create minimal test data needed for each test
- Use factories or fixtures for complex data
- Don't rely on production data
- Clean up after tests (usually automatic)

### 3. Assertions
- Use specific assertions (`assertEqual`, `assertIn`, etc.)
- Test both positive and negative cases
- Verify error conditions
- Check edge cases

### 4. Test Independence
- Each test should be independent
- Don't rely on test execution order
- Use fresh data for each test
- Reset any global state

### 5. Mocking
```python
from unittest.mock import Mock, patch

class MyTestsWithMocking(TestCase):
    @patch('myapp.external_service.call_api')
    def test_with_mocked_api(self, mock_api):
        """Test with mocked external dependency"""
        mock_api.return_value = {'status': 'success'}
        
        # Test code that calls the API
        result = my_function_that_calls_api()
        
        # Verify mock was called
        mock_api.assert_called_once()
        self.assertEqual(result, 'success')
```

## Test Summary

The Zestora test suite provides comprehensive coverage with:

- **113 total tests** covering all major functionality
- **Model tests** for data integrity and relationships
- **Form tests** for user input validation
- **View tests** for HTTP request/response handling
- **Selenium tests** for end-to-end user interactions
- **Integration tests** for component interactions

All tests pass successfully, ensuring code quality and catching regressions early in development.

---

**Last Updated**: October 10, 2025  
**Test Suite Version**: 1.0  
**Total Tests**: 113  
**Success Rate**: 100%