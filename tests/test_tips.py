"""
Selenium tests for Zestora tips functionality
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.base_selenium import SeleniumTestCase


@pytest.mark.selenium
class TestTips(SeleniumTestCase):
    """Test cooking tips functionality"""
    
    def test_cooking_tips_page(self):
        """Test cooking tips page loads"""
        self.driver.get(f'{self.live_server_url}/tips/')
        self.assert_page_title_contains("Cooking Tips")
        self.assert_text_in_page("Cooking Tips")
        
    def test_tips_navigation_from_navbar(self):
        """Test tips navigation from navbar"""
        self.driver.get(self.live_server_url)
        
        # Click tips link in navbar
        tips_link = self.wait_for_clickable_element(By.PARTIAL_LINK_TEXT, "COOKING TIPS")
        tips_link.click()
        
        # Should be on tips page
        self.assert_text_in_page("Cooking Tips")
        
    def test_tips_content_display(self):
        """Test that tips content is displayed properly"""
        self.driver.get(f'{self.live_server_url}/tips/')
        
        # Check for common tip categories or content
        # This will depend on your actual tips content
        # For now, just check that the page loaded properly
        page_source = self.driver.page_source.lower()
        
        # Should contain some cooking-related terms
        cooking_terms = ['cooking', 'recipe', 'kitchen', 'ingredient', 'tip']
        found_terms = [term for term in cooking_terms if term in page_source]
        
        self.assertTrue(len(found_terms) > 0, "Page should contain cooking-related content")