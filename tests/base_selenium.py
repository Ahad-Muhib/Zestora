"""
Base test class for Selenium tests
"""
import pytest
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
class SeleniumTestCase(StaticLiveServerTestCase):
    """Base class for Selenium tests"""
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        # Set up Firefox options
        firefox_options = Options()
        firefox_options.add_argument("--headless")  # Run in headless mode
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")
        firefox_options.add_argument("--disable-gpu")
        firefox_options.add_argument("--window-size=1920,1080")
        
        # Set up the WebDriver
        cls.driver = webdriver.Firefox(options=firefox_options)
        cls.driver.implicitly_wait(10)
        
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()
        
    def setUp(self):
        """Set up test data"""
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
        
    def login_user(self, username, password):
        """Helper method to login a user"""
        self.driver.get(f'{self.live_server_url}/accounts/login/')
        
        username_field = self.wait_for_element(By.NAME, 'login')
        password_field = self.driver.find_element(By.NAME, 'password')
        
        username_field.send_keys(username)
        password_field.send_keys(password)
        
        login_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        login_button.click()
        
    def assert_page_title_contains(self, expected_text):
        """Assert that page title contains expected text"""
        assert expected_text.lower() in self.driver.title.lower()
        
    def assert_element_present(self, by, value):
        """Assert that an element is present on the page"""
        element = self.wait_for_element(by, value)
        assert element is not None
        
    def assert_text_in_page(self, text):
        """Assert that text is present in page source"""
        assert text in self.driver.page_source