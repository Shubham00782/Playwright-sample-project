# Playwright Automation Framework

This repository contains a robust, scalable Python automation testing framework built using [Playwright](https://playwright.dev/python/) and [Pytest](https://docs.pytest.org/). It is designed using the Page Object Model (POM) design pattern and features hybrid UI and API testing capability, data-driven testing, random data generation, and rich reporting via Allure.

---

## 🌟 Features
* **Playwright + Pytest**: Fast, reliable, and asynchronous-ready browser automation.
* **Unified UI & API Testing**:
  * Execute API queries mid-test to seed data, complete backend setup, or verify states while a UI browser is open.
  * Run pure standalone API tests without opening a browser to save time and compute power.
* **Page Object Model (POM)**: Clean separation of test logic (`testcases/`), page actions (`pages/`), and UI element selectors (`locators/`).
* **Rich Reporting**: Automatically captures screenshots, videos, and traces on test failures and integrates them into [Allure Reports](https://allurereport.org/).
* **Data-Driven Testing (DDT)**: Read and write test data directly from Excel files or external JSON payloads.
* **Dynamic Data Generation**: Built-in integration with `Faker` to generate random users, addresses, and emails on the fly.
* **Centralized Configuration**: Manage base URLs, credentials, and API environment endpoints using `config/config.ini`.
* **Parallel Execution**: Run tests in parallel using `pytest-xdist` to speed up execution times.

---

## 📖 Guides and Documentation
For detailed step-by-step developer and QA onboarding instructions, refer to:
* 🖥️ [UI Testing Onboarding Guide](documentation/UI_Testing_Guide.md)
* 🔌 [API Testing Integration Guide](documentation/API_Testing_Guide.md)

---

## 🛠️ Prerequisites
Before setting up the project, ensure you have the following installed:
* **Python 3.8+**: [Download here](https://www.python.org/downloads/)
* **Node.js**: [Download here](https://nodejs.org/) (Required to install and serve Allure reports)

---

## 🚀 Setup Instructions

**1. Clone the repository**
```bash
git clone <repository_url>
cd "Playwright Sample Project"
```

**2. Set up a virtual environment**
```bash
python -m venv .venv

# Activate on Windows:
.venv\Scripts\activate

# Activate on macOS/Linux:
source .venv/bin/activate
```

**3. Install Python Dependencies**
```bash
pip install -r requirements.txt
```

**4. Install Playwright Browsers**
This downloads the browser binaries (Chromium, Firefox, WebKit) required by Playwright.
```bash
playwright install
```

**5. Install Allure Command Line**
You need the Allure CLI to view the generated HTML reports.
```bash
npm install -g allure-commandline --save-dev
# Alternatively, on Windows using scoop: scoop install allure
```

---

## 💻 Running Tests

By default, the framework is configured (via `pytest.ini`) to run in **Chromium**, in **headed** mode, and save results to `reports/allure-results`.

**Run all tests (UI + API):**
```bash
pytest
```

**Run only UI Tests:**
```bash
pytest testcases/test_login_sample_class.py
```

**Run only Standalone API Tests (runs without launching a browser):**
```bash
pytest testcases/test_api_booking.py -v
```

**Run a specific test case method:**
```bash
pytest testcases/test_login_sample_class.py::TestLoginSample::test_create_booking_via_api -v
```

**Run tests in headless mode:**
```bash
pytest --headed=false
```

**Run tests across multiple CPU cores (Parallel Execution):**
```bash
pytest -n auto
```

---

## 📊 Viewing Test Reports

After a test run completes, raw JSON data is saved in `reports/allure-results/`. To view the interactive dashboard with screenshots and videos attached to failures, run:

```bash
allure serve reports/allure-results
```
This will process the data and automatically open the report in your default web browser.

---

## 📁 Project Structure

```text
├── config/                  # Configuration files
│   ├── config.ini           # Stores base URLs for Environment and REST API
│   └── .env                 # Stores Credentials
├── documentation/           # Onboarding guides for QA Engineers
│   ├── UI_Testing_Guide.md  # Detailed POM setup and test creation guide
│   └── API_Testing_Guide.md # Playwright APIRequestContext setup guide
├── locators/                # UI Element Selectors (separated by page)
├── pages/                   # Page Object classes (methods/actions for UI)
├── reports/                 # Output directory for test artifacts
│   ├── allure-results/      # Raw Allure data
│   ├── screenshots/         # Captured screenshots on failure
│   ├── traces/              # Playwright trace zips
│   └── videos/              # Video recordings of tests
├── testcases/               # Pytest test scripts
│   ├── test_login_sample_class.py  # Mixed UI + API test class
│   └── test_api_booking.py  # Standalone API test class
├── testdata/                # External test data files
│   ├── test.xlsx            # Excel test data
│   └── booking_payload.json # External JSON payload for restful-booker
├── utils/                   # Helper functions
│   ├── config_reader.py     # Parses config.ini
│   ├── json_reader.py       # Parses JSON files with automated testdata path resolution
│   ├── csv_reader.py        # Parses CSV files
│   ├── excel_data_reader.py # Data-driven testing helpers
│   └── random_data.py       # Faker data generator
├── .gitignore               # Ignored files/folders for git
├── conftest.py              # Pytest hooks, fixtures, and browser/API contexts setup
├── pytest.ini               # Pytest default CLI options and markers
└── requirements.txt         # Python package dependencies
```

---

## ⚙️ Configuration
The core environment setup is maintained in `config/config.ini`:
```ini
[Environment]
base_url = https://www.saucedemo.com/

[API]
base_url_api = https://restful-booker.herokuapp.com
```

You can easily switch these URLs when testing different environments (e.g., Staging vs. Production). Pytest default flags (like `--browser` or `--video` settings) are maintained in `pytest.ini`.
