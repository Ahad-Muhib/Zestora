"""
Selenium tests for Zestora community functionality
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.base_selenium import SeleniumTestCase
from userprofile.models import UserProfile


@pytest.mark.selenium
class TestCommunity(SeleniumTestCase):
    """Test community functionality"""
    
    def setUp(self):
        super().setUp()
        # Get or create user profile for test user (base class creates users)
        self.user_profile, created = UserProfile.objects.get_or_create(
            user=self.test_user,
            defaults={
                'bio': "Test user bio",
                'location': "Test City"
            }
        )
        
    def test_community_home_page(self):
        """Test community home page loads"""
        self.driver.get(f'{self.live_server_url}/community/')
        self.assert_page_title_contains("Community")
        self.assert_text_in_page("Community")
        
    def test_community_members_page(self):
        """Test community members page"""
        self.driver.get(f'{self.live_server_url}/community/members/')
        self.assert_text_in_page("Community Members")
        
    def test_user_profile_page(self):
        """Test user profile page loads correctly"""
        self.driver.get(f'{self.live_server_url}/community/profile/{self.test_user.id}/')
        self.assert_text_in_page("testuser")
        # Check for profile content that's actually displayed
        self.assert_page_title_contains("testuser")
        
    def test_community_navigation_from_navbar(self):
        """Test community navigation from navbar"""
        self.driver.get(self.live_server_url)
        
        # Click community dropdown
        community_dropdown = self.wait_for_clickable_element(By.PARTIAL_LINK_TEXT, "COMMUNITY")
        community_dropdown.click()
        
        # Click community home
        community_home = self.wait_for_clickable_element(By.PARTIAL_LINK_TEXT, "Community Home")
        community_home.click()
        
        # Should be on community page
        self.assert_text_in_page("Community")
        
    def test_community_members_navigation(self):
        """Test navigation to community members"""
        self.driver.get(self.live_server_url)
        
        # Click community dropdown
        community_dropdown = self.wait_for_clickable_element(By.PARTIAL_LINK_TEXT, "COMMUNITY")
        community_dropdown.click()
        
        # Click members
        members_link = self.wait_for_clickable_element(By.PARTIAL_LINK_TEXT, "Members")
        members_link.click()
        
        # Should be on members page
        self.assert_text_in_page("Community Members")