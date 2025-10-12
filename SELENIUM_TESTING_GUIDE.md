# Selenium Testing Guide for Zestora

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
pip install selenium pytest-django webdriver-manager
```

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
```

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

### Run All Selenium Tests
```bash
cd /path/to/zestora
python -m pytest tests/ --ds=zestora.settings -v
```

### Run Specific Test File
```bash
python -m pytest tests/test_authentication.py --ds=zestora.settings -v
```

### Run Specific Test Method
```bash
python -m pytest tests/test_authentication.py::TestAuthentication::test_home_page_loads --ds=zestora.settings -v
```

### Run Tests with Output (non-headless for debugging)
```bash
python -m pytest tests/ --ds=zestora.settings -v -s
```

### Run Only Selenium Tests (using markers)
```bash
python -m pytest -m selenium --ds=zestora.settings -v
```

## Configuration

### pytest.ini
The project includes a `pytest.ini` file that configures:
- Django settings module
- Test file patterns
- Custom markers for different test types
- Selenium-specific markers

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

### Common Error Messages

1. **"cannot find Firefox binary"**: Install Firefox browser
2. **"TimeoutException"**: Element not found within timeout period
3. **"NoSuchElementException"**: Element selector is incorrect
4. **"WebDriverException"**: Browser driver issues

### Debug Commands
```bash
# Test Firefox installation
firefox --version

# Run single test with verbose output
python -m pytest tests/test_authentication.py::TestAuthentication::test_home_page_loads --ds=zestora.settings -v -s

# Check Django settings
python manage.py check

# Verify test database creation
python manage.py test --keepdb --debug-mode
```

## Best Practices

1. **Page Object Pattern**: Consider creating page objects for complex pages
2. **Test Independence**: Each test should be able to run independently
3. **Meaningful Names**: Use descriptive test method names
4. **Single Responsibility**: Each test should test one specific functionality
5. **Clean Assertions**: Use appropriate assertion methods
6. **Documentation**: Comment complex test scenarios

This testing framework provides a solid foundation for ensuring your Zestora application works correctly across different browsers and user scenarios.