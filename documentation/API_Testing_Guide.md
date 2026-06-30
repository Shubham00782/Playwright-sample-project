# Playwright API Testing Guide

A practical reference for how **API testing** is wired into this Playwright + pytest project.

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [How It Works — The `api_context` Fixture](#2-how-it-works--the-api_context-fixture)
3. [Configuration: `base_url_api`](#3-configuration-base_url_api)
4. [Externalising Payloads — JSON Test Data](#4-externalising-payloads--json-test-data)
5. [Pattern A — API call *inside* a UI test (mixed)](#5-pattern-a--api-call-inside-a-ui-test-mixed)
6. [Pattern B — Pure API tests in a dedicated file](#6-pattern-b--pure-api-tests-in-a-dedicated-file)
7. [File Structure Summary](#7-file-structure-summary)
8. [Running the Tests](#8-running-the-tests)
9. [Best Practices Checklist](#9-best-practices-checklist)

---

## 1. Architecture Overview

```
conftest.py
  └─ api_context fixture          ← shared, function-scoped
       ├─ reads base_url_api from config/config.ini  [API]
       ├─ starts a Playwright instance (no browser)
       ├─ creates APIRequestContext (pre-configured base URL + headers)
       └─ disposes everything automatically after each test

testdata/
  └─ booking_payload.json         ← payload kept outside test code

testcases/
  ├─ test_login_sample_class.py   ← Pattern A: API mid-session (UI + API)
  └─ test_api_booking.py          ← Pattern B: pure API tests
```

The key idea is that **Playwright's `APIRequestContext`** is independent of the browser. It can be used:
- Alongside an open browser page (for backend seeding / teardown during UI tests), or
- Completely standalone (no browser launched at all).

---

## 2. How It Works — The `api_context` Fixture

Defined in `conftest.py`:

```python
@pytest.fixture(scope="function")
def api_context(request):
    base_url_api = ConfigReader.read_config("API", "base_url_api")

    playwright = sync_playwright().start()

    context = playwright.request.new_context(
        base_url=base_url_api,
        ignore_https_errors=True,
        extra_http_headers={
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    )

    yield context          # test runs here

    context.dispose()      # always cleans up
    playwright.stop()
```

**Why a separate `sync_playwright().start()` instead of reusing the browser's playwright instance?**  
The browser fixture (`browser_context`) may not be requested by pure API tests. Keeping the API playwright instance separate means API-only tests never spin up a browser at all — faster and more resource-efficient.

---

## 3. Configuration: `base_url_api`

`config/config.ini`:

```ini
[Environment]
base_url = https://www.saucedemo.com/

[API]
base_url_api = https://restful-booker.herokuapp.com
```

Because `base_url_api` is set on the `APIRequestContext`, every test call uses **only the path**:

```python
# ✅  Clean — path only
response = api_context.post("/booking", data=payload)
response = api_context.get("/booking/123")

# ❌  Avoid — full URL duplicates config
response = api_context.post("https://restful-booker.herokuapp.com/booking", ...)
```

To point at a different environment (staging, QA) just change `base_url_api` in `config.ini` — no test code changes required.

---

## 4. Externalising Payloads — JSON Test Data

`testdata/booking_payload.json`:

```json
{
  "firstname": "Jim",
  "lastname": "Brown",
  "totalprice": 111,
  "depositpaid": true,
  "bookingdates": {
    "checkin": "2018-01-01",
    "checkout": "2019-01-01"
  },
  "additionalneeds": "Breakfast"
}
```

**Loading in a test:**

```python
from utils.json_reader import read_testdata_json

# Resolve path and load json from testdata folder in a single helper call
payload = read_testdata_json("booking_payload.json")
```

**Why keep payload in a JSON file instead of inline in the test?**

| Inline dict | External JSON file |
|---|---|
| Clutters test logic | Test stays readable |
| Must edit Python to change data | Data team / QA can edit JSON directly |
| Hard to reuse across tests | Shared by multiple test files |
| No syntax highlighting for data | JSON editors provide validation |

---

## 5. Pattern A — API call *inside* a UI test (mixed)

File: `testcases/test_login_sample_class.py`

```
TestLoginSample
  ├─ setup (autouse)                     — opens browser, navigates to base_url
  ├─ test_navigate_to_login_page         — UI test
  ├─ test_create_booking_via_api         — API call (browser already open)
  └─ test_valid_login_credentials        — UI test
```

**When is this pattern useful?**

- **Seeding data** before a UI test (create a record via API, then verify it in the UI).
- **Teardown** — delete test data via API after a UI test.
- **Bypassing slow UI flows** — log in via API to get a token, then hand the token to the UI.

The method signature simply asks for `api_context` as a parameter:

```python
def test_create_booking_via_api(self, api_context):
    payload = read_testdata_json("booking_payload.json")
    response = api_context.post("/booking", data=payload)
    assert response.status == 200
    ...
```

> **Note:** Both `page` (from `setup`) and `api_context` are active simultaneously. Playwright manages them independently.

---

## 6. Pattern B — Pure API tests in a dedicated file

File: `testcases/test_api_booking.py`

```
TestBookingAPI
  ├─ test_get_all_bookings          — GET /booking
  ├─ test_create_booking            — POST /booking
  └─ test_create_then_get_booking   — POST /booking → GET /booking/{id}
```

**No browser is launched** — these tests only request `api_context`, so no `page` or `browser_context` fixture is created. This makes them **very fast** and suitable for running in CI on every commit.

```python
class TestBookingAPI:

    def test_get_all_bookings(self, api_context):
        response = api_context.get("/booking")
        assert response.status == 200
        bookings = response.json()
        assert len(bookings) > 0
        for item in bookings:
            assert "bookingid" in item
```

---

## 7. File Structure Summary

```
Playwright Sample Project/
│
├─ config/
│   └─ config.ini                  ← [API] base_url_api added here
│
├─ testdata/
│   └─ booking_payload.json        ← NEW: externalised POST payload
│
├─ testcases/
│   ├─ test_login_sample_class.py  ← MODIFIED: API test added (Pattern A)
│   └─ test_api_booking.py         ← NEW: standalone API tests (Pattern B)
│
├─ utils/
│   ├─ config_reader.py            ← reads config.ini (unchanged)
│   └─ json_reader.py              ← reads JSON files + helper functions
│
└─ conftest.py                     ← MODIFIED: api_context fixture added
```

---

## 8. Running the Tests

```powershell
# Run ALL tests (UI + API)
pytest

# Run only the standalone API tests (no browser)
pytest testcases/test_api_booking.py -v

# Run only the class-based tests (UI + inline API)
pytest testcases/test_login_sample_class.py -v

# Run only the API test inside the UI class
pytest testcases/test_login_sample_class.py::TestLoginSample::test_create_booking_via_api -v

# Generate Allure report
pytest --alluredir=reports/allure_results
allure serve reports/allure_results
```

---

## 9. Best Practices Checklist

- [x] **Central base URL** — `base_url_api` in `config.ini`, not hardcoded in tests.
- [x] **Shared fixture** — `api_context` in `conftest.py` so every test file can use it.
- [x] **Auto-dispose** — `context.dispose()` + `playwright.stop()` called in fixture teardown.
- [x] **External payloads** — JSON files in `testdata/`, loaded via `read_testdata_json()`.
- [x] **Assertion messages** — every `assert` carries a human-readable failure message.
- [x] **Logging** — `logging.info/error` used instead of bare `print` for structured output.
- [x] **No browser for pure API tests** — `TestBookingAPI` never requests `page`, so no browser is spun up.
- [x] **Descriptive docstrings** — each test documents endpoint, purpose, and assertions.
