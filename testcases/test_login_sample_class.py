import pytest
from pages.login_page import LoginPage
import logging

class TestLoginSample:

    @pytest.fixture(autouse=True)
    def setup(self, page):
        """
        Setup fixture that automatically initializes the LoginPage 
        instance before each test method is executed.
        """
        self.page = page
        self.login_page = LoginPage(page, page)

    def test_navigate_to_login_page(self):
        """
        Test Case: Verify navigation to Login page and title.
        Description: This test ensures that the application navigates 
                     to the correct login URL and that the page title matches 'Swag Labs'.
        """
        try:
            self.login_page.verify_title("Swag Labs")
            
            # Additional explicit assertion
            current_title = self.page.title()
            assert "Swag Labs" in current_title, f"Expected 'Swag Labs' in title, but got '{current_title}'"
            
            logging.info("Successfully navigated and verified page title.")
        except AssertionError as ae:
            logging.error(f"Assertion failed: {str(ae)}")
            pytest.fail(f"Assertion failed: {str(ae)}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}")
            pytest.fail(f"Failed to navigate and verify title: {str(e)}")

    def test_valid_login_credentials(self):
        """
        Test Case: Verify valid login credentials.
        Description: This test uses standard user credentials to log in 
                     and asserts that the login process completes successfully by checking the URL.
        """
        try:
            self.login_page.login("standard_user", "secret_sauce")
            
            # Assert that the user is redirected to the inventory page after a successful login
            assert "inventory" in self.page.url, "User was not redirected to the inventory page after login."
            
            logging.info("Successfully logged in with valid credentials.")
        except AssertionError as ae:
            logging.error(f"Assertion failed during login: {str(ae)}")
            pytest.fail(f"Assertion failed during login: {str(ae)}")
        except Exception as e:
            logging.error(f"Login process failed with an exception: {str(e)}")
            pytest.fail(f"Login process failed with an exception: {str(e)}")