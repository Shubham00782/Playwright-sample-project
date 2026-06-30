# UI Testing Guide

> A step-by-step reference for **new QA engineers** joining this project.  
> This guide explains the Page Object Model structure, how UI tests are organised,  
> and the exact steps to add a brand-new UI test from scratch.

---

## Table of Contents

1. [How the Framework Is Organised](#1-how-the-framework-is-organised)
2. [The Page Object Model (POM) Pattern](#2-the-page-object-model-pom-pattern)
3. [Layer-by-Layer File Walkthrough](#3-layer-by-layer-file-walkthrough)
   - [Locators](#31-locators)
   - [Pages (Page Objects)](#32-pages-page-objects)
   - [Test Cases](#33-test-cases)
4. [conftest.py — Shared Fixtures](#4-conftestpy--shared-fixtures)
5. [Configuration](#5-configuration)
6. [How to Add a New UI Test — Step-by-Step](#6-how-to-add-a-new-ui-test--step-by-step)
7. [Running Tests](#7-running-tests)
8. [Test Artifacts (Screenshots, Videos, Traces)](#8-test-artifacts-screenshots-videos-traces)
9. [Do's and Don'ts](#9-dos-and-donts)

---

## 1. How the Framework Is Organised

```
Playwright Sample Project/
│
├── config/                        # Environment configuration
│   └── config.ini                 # base_url, base_url_api
│
├── locators/                      # CSS/XPath selectors (one file per page)
│   └── login_locators.py
│
├── pages/                         # Page Object classes (actions/methods)
│   ├── base_page.py               # Shared base: click, fill, navigate …
│   └── login_page.py              # Login-specific actions
│
├── testcases/                     # Pytest test scripts
│   ├── test_login_sample_class.py # Class-based UI + inline API tests
│   ├── test_login_sample_function.py # Function-based UI tests
│   └── test_api_booking.py        # Pure API tests (no browser)
│
├── testdata/                      # External test data files
│   ├── test.xlsx                  # Excel data for DDT tests
│   └── booking_payload.json       # JSON payload for API tests
│
├── utils/                         # Reusable helper utilities
│   ├── config_reader.py           # Reads config.ini
│   ├── json_reader.py             # JSON + testdata path helpers
│   ├── csv_reader.py              # CSV reader
│   ├── excel_data_reader.py       # Excel reader for DDT
│   └── random_data.py             # Faker-based random data generator
│
├── documentation/                 # Guides for QA engineers (you are here)
│   ├── UI_Testing_Guide.md        ← this file
│   └── API_Testing_Guide.md       ← API testing reference
│
├── reports/                       # Auto-generated test output
│   ├── allure-results/
│   ├── screenshots/
│   ├── traces/
│   └── videos/
│
├── conftest.py                    # Pytest fixtures (browser, page, api_context)
├── pytest.ini                     # Default CLI options and markers
└── requirements.txt               # Python dependencies
```

---

## 2. The Page Object Model (POM) Pattern

The framework follows a **strict three-layer separation**:

```
┌──────────────────────────────────────────────────────┐
│  LAYER 1 — locators/         CSS/XPath selectors     │
│  Where UI element addresses live                     │
├──────────────────────────────────────────────────────┤
│  LAYER 2 — pages/            Page Object classes     │
│  Where actions on a page are implemented             │
├──────────────────────────────────────────────────────┤
│  LAYER 3 — testcases/        Pytest test scripts     │
│  Where test scenarios and assertions are written     │
└──────────────────────────────────────────────────────┘
```

**Why this matters:**  
If a button ID changes on the login page, you fix it in **one place** (`login_locators.py`) and every test that uses it automatically gets the update — without touching any test file.

---

## 3. Layer-by-Layer File Walkthrough

### 3.1 Locators

**File:** `locators/login_locators.py`

```python
class LoginLocators:
    # Inputs
    EMAIL_INPUT    = '//input[@id="user-name"]'
    PASSWORD_INPUT = '//input[@id="password"]'

    # Buttons
    LOGIN_BUTTON   = '//input[@id="login-button"]'
```

- One class per page, matching the page name.
- Constants are `UPPER_SNAKE_CASE`.
- Use XPath (`//...`) or CSS selectors (`css=...`).
- **Never hardcode selectors inside page classes or tests.**

---

### 3.2 Pages (Page Objects)

**File:** `pages/base_page.py`  
The root class all page objects inherit from. It wraps common Playwright actions:

| Method | What it does |
|---|---|
| `navigate(path)` | Goes to `base_url + path` |
| `click(locator)` | Waits then clicks an element |
| `fill_text(locator, text)` | Fast-fills an input field |
| `type_text(locator, text)` | Character-by-character typing (simulates real user) |
| `get_text(locator)` | Returns visible text of an element |
| `is_visible(locator)` | Returns `True`/`False` |
| `verify_title(title)` | Asserts the page title matches |
| `wait_for_selector(locator, state)` | Waits for element to reach a state |

**File:** `pages/login_page.py`

```python
from pages.base_page import BasePage
from locators.login_locators import LoginLocators

class LoginPage(BasePage):
    def __init__(self, page, base_url):
        super().__init__(page, base_url)
        self.locators = LoginLocators

    def login(self, email: str, password: str):
        """Fills in credentials and submits the login form."""
        self.fill_text(self.locators.EMAIL_INPUT, email)
        self.fill_text(self.locators.PASSWORD_INPUT, password)
        self.click(self.locators.LOGIN_BUTTON)
```

Every page object follows the same pattern:
1. Inherit `BasePage`.
2. Import the matching locator class.
3. Write one method per **user action** (not per element).

---

### 3.3 Test Cases

**File:** `testcases/test_login_sample_class.py`

```python
class TestLoginSample:

    @pytest.fixture(autouse=True)
    def setup(self, page):
        """Runs before every test — initialises the page object."""
        self.page = page
        self.login_page = LoginPage(page, page)   # page fixture from conftest.py

    def test_navigate_to_login_page(self):
        self.login_page.verify_title("Swag Labs")
        assert "Swag Labs" in self.page.title()

    def test_valid_login_credentials(self):
        self.login_page.login("standard_user", "secret_sauce")
        assert "inventory" in self.page.url
```

Rules for test files:
- Filename starts with `test_`.
- Class name starts with `Test`.
- Method names start with `test_`.
- Tests call **page object methods**, never raw Playwright API directly.
- Assertions use plain `assert` with a message: `assert condition, "failure message"`.

---

## 4. conftest.py — Shared Fixtures

`conftest.py` is auto-loaded by pytest. It provides the fixtures your tests receive as parameters.

| Fixture | Scope | What it provides |
|---|---|---|
| `browser_context` | `function` | A Playwright browser context (with video recording if configured) |
| `page` | `function` | A browser page navigated to `base_url`; handles screenshots/traces on failure |
| `api_context` | `function` | A Playwright `APIRequestContext` pre-configured with `base_url_api` |

**How fixtures are chained:**

```
browser_context  ←  reads --browser, --headed, --video flags
       ↓
     page         ←  depends on browser_context; navigates to base_url
                      handles screenshots / video / trace on failure

api_context       ←  independent; no browser required
```

Your test simply **declares the fixture as a parameter** and pytest injects it automatically:

```python
def test_something(self, page):          # UI test — gets a browser page
def test_api_call(self, api_context):    # API test — no browser launched
def test_mixed(self, page, api_context): # Both active simultaneously
```

---

## 5. Configuration

**File:** `config/config.ini`

```ini
[Environment]
base_url     = https://www.saucedemo.com/

[API]
base_url_api = https://restful-booker.herokuapp.com
```

- `base_url` → injected into the `page` fixture; all UI tests start here.
- `base_url_api` → injected into the `api_context` fixture.
- To switch environments, **only change this file** — no test code edits needed.

**File:** `pytest.ini` (default run flags)

```ini
addopts =
    -v
    --browser=chromium
    --headed
    --video=retain-on-failure
    --screenshot=only-on-failure
    --tracing=retain-on-failure
    --alluredir=reports/allure-results
    --reruns 2
    --reruns-delay 1
```

These defaults can be overridden on the command line.

---

## 6. How to Add a New UI Test — Step-by-Step

Follow these four steps every time you add tests for a new page.

---

### Step 1 — Create the Locators file

> Skip if the page already has a locators file.

Create `locators/<page_name>_locators.py`:

```python
class CheckoutLocators:
    # Headings
    CHECKOUT_TITLE = '//span[@class="title"]'

    # Inputs
    FIRST_NAME = '//input[@id="first-name"]'
    LAST_NAME  = '//input[@id="last-name"]'
    POSTAL_CODE= '//input[@id="postal-code"]'

    # Buttons
    CONTINUE_BUTTON = '//input[@id="continue"]'
    FINISH_BUTTON   = '//button[@id="finish"]'
```

---

### Step 2 — Create the Page Object class

Create `pages/<page_name>_page.py`:

```python
from pages.base_page import BasePage
from locators.checkout_locators import CheckoutLocators

class CheckoutPage(BasePage):
    def __init__(self, page, base_url):
        super().__init__(page, base_url)
        self.locators = CheckoutLocators

    def fill_customer_info(self, first: str, last: str, postal: str):
        """Fills the customer information form."""
        self.fill_text(self.locators.FIRST_NAME, first)
        self.fill_text(self.locators.LAST_NAME, last)
        self.fill_text(self.locators.POSTAL_CODE, postal)
        self.click(self.locators.CONTINUE_BUTTON)

    def complete_order(self):
        """Clicks the Finish button to complete the order."""
        self.click(self.locators.FINISH_BUTTON)

    def get_confirmation_title(self) -> str:
        """Returns the text of the page title element."""
        return self.get_text(self.locators.CHECKOUT_TITLE)
```

---

### Step 3 — Write the Test file

Create `testcases/test_checkout.py`:

```python
import pytest
import logging
from pages.checkout_page import CheckoutPage


class TestCheckout:

    @pytest.fixture(autouse=True)
    def setup(self, page):
        """Initialises CheckoutPage before each test."""
        self.page = page
        self.checkout_page = CheckoutPage(page, page)

    def test_complete_checkout_flow(self):
        """
        Test Case : Complete the checkout process.
        Asserts   : Confirmation title is displayed after order is placed.
        """
        try:
            self.checkout_page.fill_customer_info("John", "Doe", "12345")
            self.checkout_page.complete_order()

            title = self.checkout_page.get_confirmation_title()
            assert "THANK YOU" in title.upper(), (
                f"Expected 'THANK YOU' in title, got '{title}'"
            )
            logging.info("Checkout completed successfully.")
        except AssertionError as ae:
            logging.error(f"Assertion failed: {ae}")
            pytest.fail(str(ae))
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            pytest.fail(str(e))
```

---

### Step 4 — Run your new test

```powershell
# Run just your new test file
.venv\Scripts\python.exe -m pytest testcases/test_checkout.py -v

# Run a single test method
.venv\Scripts\python.exe -m pytest testcases/test_checkout.py::TestCheckout::test_complete_checkout_flow -v
```

---

## 7. Running Tests

> On Windows, prefix with `.venv\Scripts\python.exe -m` if `pytest` is not in PATH.

```powershell
# Run all tests
pytest

# Run all tests in a single file
pytest testcases/test_login_sample_class.py -v

# Run a single test method
pytest testcases/test_login_sample_class.py::TestLoginSample::test_navigate_to_login_page -v

# Run in headless mode (no browser window)
pytest --headed=false

# Run only tests tagged with a marker
pytest -m smoke
pytest -m regression

# Run in parallel (faster for large suites)
pytest -n auto

# Generate + view Allure report
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

---

## 8. Test Artifacts (Screenshots, Videos, Traces)

All artifacts are saved under `reports/` and are managed automatically by conftest.py.

| Artifact | Folder | When saved |
|---|---|---|
| Screenshot (PNG) | `reports/screenshots/` | On test **failure** (configurable) |
| Video (WEBM) | `reports/videos/` | On test **failure** (configurable) |
| Trace (ZIP) | `reports/traces/` | On test **failure** (configurable) |

Screenshots and videos are also **attached to the Allure report** automatically — you can view them by clicking on a failed test in the Allure dashboard.

To open a Playwright trace file for debugging:
```bash
playwright show-trace reports/traces/<test_name>_trace.zip
```

---

## 9. Do's and Don'ts

| ✅ Do | ❌ Don't |
|---|---|
| Put selectors in `locators/` | Hardcode selectors in test files |
| Write one method per user action in page objects | Write assertions inside page objects |
| Use `BasePage` methods (`fill_text`, `click` …) | Call `self.page.locator(...)` directly in tests |
| Add descriptive docstrings to every test | Leave test methods without a description |
| Use `logging.info/error` for output | Use bare `print()` statements |
| Keep test data in `testdata/` | Hardcode test data inside test methods |
| Use `assert condition, "message"` with a message | Use bare `assert condition` with no context |
| Name test files `test_<feature>.py` | Name files something that doesn't start with `test_` |
