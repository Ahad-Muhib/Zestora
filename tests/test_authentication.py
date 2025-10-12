"""
Selenium tests for Zestora authentication functionality
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.base_selenium import SeleniumTestCase


@pytest.mark.selenium
class TestAuthentication(SeleniumTestCase):
    """Test authentication functionality"""
    
    def test_home_page_loads(self):
        """Test that the home page loads correctly"""
        self.driver.get(self.live_server_url)
        self.assert_page_title_contains("Zestora")
        self.assert_text_in_page("Zestora")
        
    def test_login_page_accessible(self):
        """Test that login page is accessible and has correct title"""
        self.driver.get(f'{self.live_server_url}/accounts/login/')
        self.assert_page_title_contains("Sign In")
        
    def test_user_login_success(self):
        """Test successful user login"""
        self.login_user('testuser', 'testpass123')
        
        # Wait for redirect and check we're logged in
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Logout"))
        )
        self.assert_text_in_page("Logout")
        
    def test_user_login_failure(self):
        """Test failed login with wrong credentials"""
        self.driver.get(f'{self.live_server_url}/accounts/login/')
        
        username_field = self.wait_for_element(By.NAME, 'login')
        password_field = self.driver.find_element(By.NAME, 'password')
        
        username_field.send_keys('wronguser')
        password_field.send_keys('wrongpass')
        
        login_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        login_button.click()
        
        # Should stay on login page or show error
        self.assert_text_in_page("Sign In")
        
    def test_admin_login_and_access_admin_tools(self):
        """Test admin login and access to admin tools"""
        self.login_user('testadmin', 'testpass123')
        
        # Wait for page to load and check for admin dropdown
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "admin-dropdown-btn"))
        )
        
        # Click admin dropdown
        admin_dropdown = self.driver.find_element(By.CLASS_NAME, "admin-dropdown-btn")
        admin_dropdown.click()
        
        # Check for admin menu items
        self.assert_text_in_page("Statistics")
        self.assert_text_in_page("Manage Users")
        self.assert_text_in_page("Django Admin")
        
    def test_signup_page_accessible(self):
        """Test that signup page is accessible"""
        self.driver.get(f'{self.live_server_url}/accounts/signup/')
        self.assert_page_title_contains("Signup")
        self.assert_element_present(By.NAME, 'username')
        self.assert_element_present(By.NAME, 'email')
        self.assert_element_present(By.NAME, 'password1')