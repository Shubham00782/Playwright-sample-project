import pytest
import logging
from utils.json_reader import read_testdata_json


"""
---------------------------------------------------------
Standalone API Tests — Restful Booker API
---------------------------------------------------------
This file demonstrates how to perform pure API testing with
Playwright's APIRequestContext — no browser is launched.

The api_context fixture (defined in conftest.py) handles:
  • Reading base_url_api from config/config.ini  [API]
  • Creating & disposing the APIRequestContext automatically

Test payload is externalised into testdata/booking_payload.json.
---------------------------------------------------------
"""


class TestBookingAPI:
    """
    Test suite for the Restful-Booker REST API.
    https://restful-booker.herokuapp.com/apidoc/
    """

    # ==================================================================
    # TC-API-01  GET /booking — Fetch all bookings
    # ==================================================================
    def test_get_all_bookings(self, api_context):
        """
        Test Case: Fetch all booking IDs from the API.
        Endpoint  : GET /booking
        Asserts   :
            - HTTP 200 status.
            - Response is a non-empty list.
            - Each item in the list contains a 'bookingid' key.
        """
        try:
            response = api_context.get("/booking")

            # ── Assert status ─────────────────────────────────────────
            assert response.status == 200, (
                f"Expected status 200, but got {response.status}"
            )

            response_json = response.json()

            # ── Assert the list is not empty ──────────────────────────
            assert isinstance(response_json, list), "Response body should be a list"
            assert len(response_json) > 0, "Booking list should not be empty"

            # ── Assert each item contains a bookingid ─────────────────
            for item in response_json:
                assert "bookingid" in item, (
                    f"'bookingid' key missing from list item: {item}"
                )

            logging.info(f"Fetched {len(response_json)} bookings successfully.")

        except AssertionError as ae:
            logging.error(f"Assertion failed: {str(ae)}")
            pytest.fail(f"Assertion failed: {str(ae)}")
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            pytest.fail(f"Unexpected error in test_get_all_bookings: {str(e)}")

    # ==================================================================
    # TC-API-02  POST /booking — Create a new booking
    # ==================================================================
    def test_create_booking(self, api_context):
        """
        Test Case: Create a new hotel booking via POST /booking.
        Endpoint  : POST /booking
        Payload   : Loaded from testdata/booking_payload.json
        Asserts   :
            - HTTP 200 status.
            - Response contains 'bookingid'.
            - Response 'booking' object matches the submitted payload exactly.
        """
        try:
            # ── Load payload from testdata/ folder ──────────────────────
            payload = read_testdata_json("booking_payload.json")

            # ── Send POST request ─────────────────────────────────────
            # api_context already has base_url = base_url_api from config.ini
            # so we only pass the relative path.
            response = api_context.post("/booking", data=payload)

            # ── Assert status ─────────────────────────────────────────
            assert response.status == 200, (
                f"Expected status 200, but got {response.status}"
            )

            response_json = response.json()

            # ── Assert bookingid exists ───────────────────────────────
            assert "bookingid" in response_json, (
                "'bookingid' key is missing from the API response"
            )

            # ── Assert response body matches the sent payload ─────────
            booking = response_json["booking"]
            assert booking["firstname"]               == payload["firstname"]
            assert booking["lastname"]                == payload["lastname"]
            assert booking["totalprice"]              == payload["totalprice"]
            assert booking["depositpaid"]             == payload["depositpaid"]
            assert booking["additionalneeds"]         == payload["additionalneeds"]
            assert booking["bookingdates"]["checkin"] == payload["bookingdates"]["checkin"]
            assert booking["bookingdates"]["checkout"]== payload["bookingdates"]["checkout"]

            logging.info("Booking created successfully!")
            logging.info(f"Booking ID: {response_json['bookingid']}")

        except AssertionError as ae:
            logging.error(f"Assertion failed: {str(ae)}")
            pytest.fail(f"Assertion failed: {str(ae)}")
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            pytest.fail(f"Unexpected error in test_create_booking: {str(e)}")

    # ==================================================================
    # TC-API-03  POST /booking → GET /booking/{id} — Round-trip check
    # ==================================================================
    def test_create_then_get_booking(self, api_context):
        """
        Test Case: Create a booking and then retrieve it by its ID.
        Endpoints :
            POST /booking           → Create
            GET  /booking/{id}      → Retrieve
        Asserts   :
            - Created booking can be fetched by the returned bookingid.
            - Retrieved booking matches the original payload.
        """
        try:
            payload = read_testdata_json("booking_payload.json")

            # Step 1 – Create booking
            create_response = api_context.post("/booking", data=payload)
            assert create_response.status == 200, (
                f"Create booking failed with status {create_response.status}"
            )
            create_json   = create_response.json()
            booking_id    = create_json["bookingid"]
            logging.info(f"Created booking ID: {booking_id}")

            # Step 2 – Retrieve booking by ID
            get_response = api_context.get(f"/booking/{booking_id}")
            assert get_response.status == 200, (
                f"GET /booking/{booking_id} failed with status {get_response.status}"
            )

            fetched = get_response.json()

            # Step 3 – Verify the retrieved data matches the payload
            assert fetched["firstname"]               == payload["firstname"]
            assert fetched["lastname"]                == payload["lastname"]
            assert fetched["totalprice"]              == payload["totalprice"]
            assert fetched["depositpaid"]             == payload["depositpaid"]
            assert fetched["additionalneeds"]         == payload["additionalneeds"]
            assert fetched["bookingdates"]["checkin"] == payload["bookingdates"]["checkin"]
            assert fetched["bookingdates"]["checkout"]== payload["bookingdates"]["checkout"]

            logging.info("Round-trip test passed: created and retrieved booking match.")

        except AssertionError as ae:
            logging.error(f"Assertion failed: {str(ae)}")
            pytest.fail(f"Assertion failed: {str(ae)}")
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            pytest.fail(f"Unexpected error in test_create_then_get_booking: {str(e)}")
