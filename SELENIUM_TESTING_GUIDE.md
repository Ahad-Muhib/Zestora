# Selenium Testing Guide for Zestora

## 🚀 Quick Start (TL;DR)

### Standard Testing (Fast, No Browser Window)
```bash
cd /home/muhib/muhib/project/Zestora
DJANGO_SETTINGS_MODULE=zestora.settings /home/muhib/muhib/project/Zestora/venv/bin/python -m pytest tests/ -v
```
**Expected result**: 131 tests pass in ~4-5 minutes

### Visual Testing (Watch Browser Actions)
```bash
# Basic visual demo
DJANGO_SETTINGS_MODULE=zestora.settings /home/muhib/muhib/project/Zestora/venv/bin/python -m pytest tests/test_visual_demo.py -v -s

# 🆕 User signup and recipe CRUD demo (NEW!)
DJANGO_SETTINGS_MODULE=zestora.settings /home/muhib/muhib/project/Zestora/venv/bin/python -m pytest tests/test_visual_signup_recipes.py -v -s

# Guaranteed working visual tests
DJANGO_SETTINGS_MODULE=zestora.settings /home/muhib/muhib/project/Zestora/venv/bin/python -m pytest tests/test_visual_working.py -v -s
```
**Expected result**: Browser opens, shows each test step-by-step, then closes

### 🎯 **NEW: Complete User Journey Demo**
```bash
# Watch complete user signup → login → create recipes → edit → view
DJANGO_SETTINGS_MODULE=zestora.settings /home/muhib/muhib/project/Zestora/venv/bin/python -m pytest tests/test_visual_signup_recipes.py::TestUserSignupAndRecipeCRUD::test_complete_user_signup_and_recipe_journey -v -s
```
**Shows**: Random user registration, login, recipe creation with random data, CRUD operations

---

## Overview

This guide explains how to set up and run Selenium tests for the Zestora web application. Selenium tests allow you to automate browser interactions and test your application's user interface end-to-end.

## Prerequisites

### System Requirements
- Python 3.8+
- Firefox browser installed
- Django project set up and running

### Python Dependencies
The following packages are required and should be installed in your virtual environment:

```bash
# Make sure you're in your project directory and virtual environment is activated
cd /home/muhib/muhib/project/Zestora
source venv/bin/activate

# Install required packages
pip install selenium pytest-django webdriver-manager

# Verify installation
pip list | grep -E "(selenium|pytest|django)"
```

**Note**: The virtual environment must be used for all test commands. Use the full path `/home/muhib/muhib/project/Zestora/venv/bin/python` if virtual environment is not activated.

## Test Structure

### Test Directory Structure
```
tests/
├── __init__.py                 # Makes tests a Python package
├── base_selenium.py           # Base test class with common functionality
├── test_authentication.py    # Authentication and login tests
├── test_admin.py             # Admin tools and functionality tests
├── test_recipes.py           # Recipe-related functionality tests
├── test_community.py         # Community features tests
└── test_tips.py              # Cooking tips page tests
```DJANGO_SETTINGS_MODULE=zestora.settings /home/muhib/muhib/project/Zestora/venv/bin/python -m pytest tests/test_visual_demo.py -v -s


### Base Test Class

All Selenium tests inherit from `SeleniumTestCase` which provides:

- **Firefox WebDriver setup**: Automatically configures headless Firefox
- **Test database**: Creates isolated test database for each test
- **Test users**: Creates admin and regular users for testing
- **Helper methods**: Common actions like login, waiting for elements
- **Assertions**: Custom assertions for checking page content

### Key Helper Methods

```python
# Login a user
self.login_user('username', 'password')

# Wait for elements
element = self.wait_for_element(By.ID, 'element-id')
clickable = self.wait_for_clickable_element(By.LINK_TEXT, 'Click Me')

# Assertions
self.assert_text_in_page('Expected Text')
self.assert_page_title_contains('Page Title')
self.assert_element_present(By.CLASS_NAME, 'element-class')
```

## Running Tests

**IMPORTANT**: First install required dependencies:
```bash
pip install pytest-django selenium webdriver-manager
```

### Run All Tests (Recommended)
```bash
cd /home/muhib/muhib/project/Zestora
DJANGO_SETTINGS_MODULE=zestora.settings /home/muhib/muhib/project/Zestora/venv/bin/python -m pytest tests/ -v
```

### Quick Commands (if virtual environment is activated)
```bash
# First activate virtual environment
source venv/bin/activate

# Then run tests with Django settings
DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/ -v
```

### Run Specific Test File
```bash
DJANGO_SETTINGS_MODULE=zestora.settings /home/muhib/muhib/project/Zestora/venv/bin/python -m pytest tests/test_authentication.py -v
```

### Run Specific Test Method
```bash
DJANGO_SETTINGS_MODULE=zestora.settings /home/muhib/muhib/project/Zestora/venv/bin/python -m pytest tests/test_authentication.py::TestAuthentication::test_home_page_loads -v
```

### Run Tests with Debug Output
```bash
DJANGO_SETTINGS_MODULE=zestora.settings /home/muhib/muhib/project/Zestora/venv/bin/python -m pytest tests/ -v -s
```

### Run Only Selenium Tests (using markers)
```bash
DJANGO_SETTINGS_MODULE=zestora.settings /home/muhib/muhib/project/Zestora/venv/bin/python -m pytest -m selenium -v
```

## 🎬 Visual Testing Mode

**Watch your tests run in a real browser!** Perfect for debugging, demonstrations, or understanding what tests actually do.

### Run Visual Demo Tests
```bash
# Run all visual tests - browser opens and shows each step
DJANGO_SETTINGS_MODULE=zestora.settings /home/muhib/muhib/project/Zestora/venv/bin/python -m pytest tests/test_visual_demo.py -v -s

# Run specific visual test
DJANGO_SETTINGS_MODULE=zestora.settings /home/muhib/muhib/project/Zestora/venv/bin/python -m pytest tests/test_visual_demo.py::TestVisualAuthentication::test_user_login_success_visual -v -s

# Run all tests marked as visual
DJANGO_SETTINGS_MODULE=zestora.settings /home/muhib/muhib/project/Zestora/venv/bin/python -m pytest -m visual -v -s
```

### What You'll See:
1. 🌐 **Firefox browser opens** (visible window)
2. 🏠 **Navigates to your site** automatically  
3. 🔐 **Types in forms** (username, password, search)
4. 🖱️ **Clicks buttons and links** 
5. ⏱️ **Pauses between actions** (2-3 seconds) so you can see what's happening
6. 📝 **Console output** explains each step
7. ✅ **Closes automatically** when done

### Available Visual Tests:

#### Basic Navigation & UI Tests (`test_visual_demo.py`):
- **Home page loading** - Watch the site load
- **Login process** - See username/password entry and login
- **Navigation demo** - Browse through different pages  
- **Search functionality** - Type search queries and see results
- **Recipe page access** - Navigate to recipe sections

#### Guaranteed Working Tests (`test_visual_working.py`):
- **Browser automation demo** - Window resizing, scrolling, screenshots
- **Page navigation** - Visit different sections of the site
- **Complete user journey** - End-to-end site exploration
- **Screenshot collection** - Automatic screenshot capture

#### User Signup & Recipe CRUD (`test_visual_signup_recipes.py`):
- **🆕 User signup with random data** - Watch complete registration process
- **🔐 User login** - Automated login after signup
- **📝 Recipe creation** - Fill out complete recipe form with random data
- **👀 Recipe viewing** - Navigate to created recipes
- **✏️ Recipe editing** - Update recipe information
- **🗑️ Recipe management** - Complete CRUD operations

### Run Specific Visual Test Categories:
```bash
# User signup and recipe management journey
DJANGO_SETTINGS_MODULE=zestora.settings /home/muhib/muhib/project/Zestora/venv/bin/python -m pytest tests/test_visual_signup_recipes.py::TestUserSignupAndRecipeCRUD::test_complete_user_signup_and_recipe_journey -v -s

# Recipe CRUD operations only
DJANGO_SETTINGS_MODULE=zestora.settings /home/muhib/muhib/project/Zestora/venv/bin/python -m pytest tests/test_visual_signup_recipes.py::TestRecipeCRUDOperations::test_recipe_crud_demo -v -s

# Browser automation demos
DJANGO_SETTINGS_MODULE=zestora.settings /home/muhib/muhib/project/Zestora/venv/bin/python -m pytest tests/test_visual_working.py::TestVisualUserJourney::test_complete_user_journey_demo -v -s
```

### Convert Any Test to Visual Mode:
Replace `SeleniumTestCase` with `VisualSeleniumTestCase`:
```python
# Change this:
from tests.base_selenium import SeleniumTestCase

# To this:
from tests.base_selenium_visual import VisualSeleniumTestCase

# Add visual marker:
@pytest.mark.visual
class TestMyFeature(VisualSeleniumTestCase):
    # Your tests here - they'll now run visually!
```

## Configuration

### Important Setup Notes
1. **Django Settings**: Must be set via environment variable `DJANGO_SETTINGS_MODULE=zestora.settings`
2. **Virtual Environment**: Always use the virtual environment Python (`/home/muhib/muhib/project/Zestora/venv/bin/python`)
3. **Firefox Browser**: Must be installed on your system for Selenium tests

### pytest.ini
The project includes a `pytest.ini` file that configures:
- Django settings module (`DJANGO_SETTINGS_MODULE = zestora.settings`)
- Test file patterns
- Custom markers for different test types
- Selenium-specific markers

**Note**: Despite pytest.ini configuration, you still need to set the environment variable when running tests.

### Firefox Options
The base test class configures Firefox with:
- Headless mode (no GUI)
- Optimized performance settings
- Consistent window size (1920x1080)

## Writing New Tests

### Basic Test Structure
```python
import pytest
from selenium.webdriver.common.by import By
from tests.base_selenium import SeleniumTestCase

@pytest.mark.selenium
class TestMyFeature(SeleniumTestCase):
    """Test my application feature"""
    
    def test_feature_works(self):
        """Test that my feature works correctly"""
        # Navigate to page
        self.driver.get(f'{self.live_server_url}/my-page/')
        
        # Check page loaded
        self.assert_text_in_page('Expected Content')
        
        # Interact with elements
        button = self.wait_for_clickable_element(By.ID, 'my-button')
        button.click()
        
        # Verify result
        self.assert_text_in_page('Success Message')
```

### Test Data Setup
```python
def setUp(self):
    super().setUp()
    # Create additional test data specific to your tests
    from myapp.models import MyModel
    self.test_object = MyModel.objects.create(
        name='Test Object',
        user=self.test_user
    )
```

## Available Test Cases

### Authentication Tests
- Home page loading
- Login page accessibility
- User login success/failure
- Admin login and access
- Signup page functionality

### Admin Tests
- Admin dashboard access
- Admin dropdown navigation
- User management features
- System tools access
- Permission restrictions

### Recipe Tests
- Recipe list and detail pages
- Recipe search functionality
- Add recipe authentication
- Category browsing

### Community Tests
- Community home page
- Member listing
- User profiles
- Navigation testing

### Tips Tests
- Cooking tips page
- Content display
- Navigation functionality

## Debugging Tests

### Common Issues and Solutions

1. **Element Not Found**: Use explicit waits instead of implicit waits
   ```python
   element = self.wait_for_element(By.ID, 'element-id')
   ```

2. **Test Database Issues**: Ensure proper test isolation
   ```python
   def setUp(self):
       super().setUp()  # Always call parent setUp
   ```

3. **Timing Issues**: Add appropriate waits for dynamic content
   ```python
   self.wait_for_clickable_element(By.LINK_TEXT, 'Dynamic Link')
   ```

### Running Tests in Visible Mode
For debugging, you can modify the base test class to run Firefox in visible mode:
```python
# In base_selenium.py, comment out the headless option
# firefox_options.add_argument("--headless")
```

### Test Output and Logging
Use `-s` flag to see print statements and detailed output:
```bash
python -m pytest tests/test_authentication.py --ds=zestora.settings -v -s
```

## Performance Tips

1. **Use Headless Mode**: Keeps tests fast by not rendering GUI
2. **Minimize Waits**: Use appropriate timeout values
3. **Clean Up Resources**: Base class handles WebDriver cleanup
4. **Isolate Tests**: Each test gets fresh database state
5. **Use Specific Selectors**: Prefer ID and class selectors over XPath

## Continuous Integration

For CI/CD pipelines, ensure:
- Firefox is installed in the CI environment
- Use headless mode (default in our setup)
- Set appropriate timeouts for slower CI environments
- Consider using Docker containers for consistent environments

## Troubleshooting

### Common Error Messages and Solutions

1. **"cannot find Firefox binary"**: 
   ```bash
   # Install Firefox browser
   sudo apt install firefox  # Ubuntu/Debian
   # or download from https://www.mozilla.org/firefox/
   ```

2. **"unrecognized arguments: --ds=zestora.settings"**:
   ```bash
   # Use environment variable instead
   DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/ -v
   ```

3. **"ModuleNotFoundError: No module named 'django'"**:
   ```bash
   # Use virtual environment Python
   /home/muhib/muhib/project/Zestora/venv/bin/python -m pytest tests/ -v
   ```

4. **"Requested setting INSTALLED_APPS, but settings are not configured"**:
   ```bash
   # Set Django settings
   DJANGO_SETTINGS_MODULE=zestora.settings python -m pytest tests/ -v
   ```

### Debug Commands
```bash
# Test Firefox installation
firefox --version

# Run single test with verbose output
DJANGO_SETTINGS_MODULE=zestora.settings /home/muhib/muhib/project/Zestora/venv/bin/python -m pytest tests/test_authentication.py::TestAuthentication::test_home_page_loads -v -s

# Check Django settings
python manage.py check

# Verify dependencies
pip list | grep -E "(selenium|pytest|django)"
```

## Best Practices

1. **Page Object Pattern**: Consider creating page objects for complex pages
2. **Test Independence**: Each test should be able to run independently
3. **Meaningful Names**: Use descriptive test method names
4. **Single Responsibility**: Each test should test one specific functionality
5. **Clean Assertions**: Use appropriate assertion methods
6. **Documentation**: Comment complex test scenarios

This testing framework provides a solid foundation for ensuring your Zestora application works correctly across different browsers and user scenarios.