import pytest
from pages.login_page import LoginPage
from utils.json_reader import read_testdata_json
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

    def test_create_booking_via_api(self, api_context):
        """
        Test Case: Create a booking via API while the browser is open.
        Description: Demonstrates how to call a backend REST API mid-session
                     (using Playwright's APIRequestContext) alongside the live
                     UI browser context.  The request payload is loaded from an
                     external JSON file kept in the testdata/ folder.

        Steps:
            1.  Load payload from testdata/booking_payload.json.
            2.  POST to /booking on the restful-booker API.
            3.  Assert HTTP 200 status.
            4.  Assert the response contains a bookingid.
            5.  Assert every field in the response matches the payload.
        """
        try:
            # ── Load payload from testdata/ folder ───────────────────────────
            payload = read_testdata_json("booking_payload.json")

            # ── Send POST request ─────────────────────────────────────────────
            # api_context already has base_url set to the API base URL from config.ini
            # so we only pass the path here.
            response = api_context.post("/booking", data=payload)

            # ── Assert Status Code ────────────────────────────────────────────
            assert response.status == 200, (
                f"Expected status 200, but got {response.status}"
            )

            response_json = response.json()

            # ── Assert bookingid exists in response ───────────────────────────
            assert "bookingid" in response_json, (
                "'bookingid' key is missing from the API response"
            )

            # ── Assert response body matches the sent payload ─────────────────
            booking = response_json["booking"]
            assert booking["firstname"]   == payload["firstname"]
            assert booking["lastname"]    == payload["lastname"]
            assert booking["totalprice"]  == payload["totalprice"]
            assert booking["depositpaid"] == payload["depositpaid"]
            assert booking["additionalneeds"] == payload["additionalneeds"]
            assert booking["bookingdates"]["checkin"]  == payload["bookingdates"]["checkin"]
            assert booking["bookingdates"]["checkout"] == payload["bookingdates"]["checkout"]

            logging.info("Booking created successfully via API!")
            logging.info(f"Booking ID: {response_json['bookingid']}")

        except AssertionError as ae:
            logging.error(f"API assertion failed: {str(ae)}")
            pytest.fail(f"API assertion failed: {str(ae)}")
        except Exception as e:
            logging.error(f"API test failed with exception: {str(e)}")
            pytest.fail(f"API test failed with exception: {str(e)}")


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