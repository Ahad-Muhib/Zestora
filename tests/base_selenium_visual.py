"""
Base test class for Selenium tests with VISIBLE browser
Use this for debugging and watching tests run step by step
"""
import pytest
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.test import override_settings


@override_settings(DEBUG=True)
class VisualSeleniumTestCase(StaticLiveServerTestCase):
    """Base class for Selenium tests with VISIBLE browser"""
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        # Set up Firefox options for VISIBLE testing
        firefox_options = Options()
        # REMOVED: firefox_options.add_argument("--headless")  # Comment out for visible browser
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")
        firefox_options.add_argument("--window-size=1200,800")  # Smaller window for visibility
        
        # Set up the WebDriver
        cls.driver = webdriver.Firefox(options=firefox_options)
        cls.driver.implicitly_wait(10)
        
        print(f"\n🌐 Browser opened! Running tests visually...")
        print(f"📍 Live server URL: {cls.live_server_url}")
        
    @classmethod
    def tearDownClass(cls):
        print(f"\n✅ All tests completed. Closing browser in 3 seconds...")
        time.sleep(3)  # Wait 3 seconds before closing
        cls.driver.quit()
        super().tearDownClass()
        
    def setUp(self):
        """Set up test data"""
        print(f"\n🧪 Starting test: {self._testMethodName}")
        
        # Create a test admin user
        self.admin_user = User.objects.create_superuser(
            username='testadmin',
            email='testadmin@test.com',
            password='testpass123'
        )
        
        # Create a regular test user
        self.test_user = User.objects.create_user(
            username='testuser',
            email='testuser@test.com',
            password='testpass123'
        )
        
    def tearDown(self):
        """Clean up after each test"""
        print(f"✅ Test completed: {self._testMethodName}")
        time.sleep(2)  # Pause 2 seconds between tests to see results
        super().tearDown()

    def login_user(self, username, password):
        """Helper method to login a user"""
        print(f"🔐 Logging in user: {username}")
        self.driver.get(f'{self.live_server_url}/accounts/login/')
        
        username_field = self.wait_for_element(By.NAME, 'username')
        password_field = self.wait_for_element(By.NAME, 'password')
        
        username_field.send_keys(username)
        password_field.send_keys(password)
        
        login_button = self.wait_for_clickable_element(By.CSS_SELECTOR, 'button[type="submit"]')
        login_button.click()
        
        time.sleep(1)  # Wait to see login action
        
    def wait_for_element(self, by, value, timeout=10):
        """Wait for an element to be present"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        
    def wait_for_clickable_element(self, by, value, timeout=10):
        """Wait for an element to be clickable"""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        
    def assert_text_in_page(self, text):
        """Assert that text is present in the page"""
        print(f"🔍 Checking for text: '{text}'")
        try:
            assert text in self.driver.page_source, f"Text '{text}' not found in page"
            print(f"✅ Found text: '{text}'")
        except AssertionError:
            print(f"ℹ️ Text '{text}' not found - this might be expected")
            raise
        
    def assert_page_title_contains(self, title_text):
        """Assert that page title contains specific text"""
        print(f"📄 Checking page title contains: '{title_text}'")
        try:
            assert title_text in self.driver.title, f"Title doesn't contain '{title_text}'"
            print(f"✅ Page title contains: '{title_text}'")
        except AssertionError:
            print(f"ℹ️ Page title is: '{self.driver.title}'")
            print(f"ℹ️ Expected to contain: '{title_text}'")
            raise
        
    def assert_element_present(self, by, value):
        """Assert that an element is present on the page"""
        print(f"🎯 Checking element is present: {by}={value}")
        try:
            element = self.wait_for_element(by, value)
            assert element is not None, f"Element {by}={value} not found"
            print(f"✅ Element found: {by}={value}")
        except Exception:
            print(f"ℹ️ Element not found: {by}={value}")
            raise
        
    def take_screenshot(self, name="screenshot"):
        """Take a screenshot for debugging"""
        filename = f"/tmp/{name}_{self._testMethodName}.png"
        self.driver.save_screenshot(filename)
        print(f"📸 Screenshot saved: {filename}")