# Playwright Automation Framework

This repository contains a robust, scalable Python automation testing framework built using [Playwright](https://playwright.dev/python/) and [Pytest](https://docs.pytest.org/). It is designed using the Page Object Model (POM) design pattern and features data-driven testing, random data generation, and rich reporting via Allure.

## 🌟 Features
* **Playwright + Pytest**: Fast, reliable, and asynchronous-ready browser automation.
* **Page Object Model (POM)**: Clean separation of test logic (`testcases/`), page actions (`pages/`), and UI element selectors (`locators/`).
* **Rich Reporting**: Automatically captures screenshots, videos, and traces on test failures and integrates them into [Allure Reports](https://allurereport.org/).
* **Data-Driven Testing (DDT)**: Read and write test data directly from Excel files using `openpyxl`.
* **Dynamic Data Generation**: Built-in integration with `Faker` to generate random users, addresses, and emails on the fly.
* **Centralized Configuration**: Easily manage base URLs and environments using `config/config.ini`.
* **Parallel Execution**: Run tests in parallel using `pytest-xdist` to speed up execution times.

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
cd "Opencart Playwright Main"
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

**Run all tests:**
```bash
pytest
```

**Run a specific test file:**
```bash
pytest testcases/test_login_sample_class.py
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
│   └── config.ini           # Stores environment variables like base_url
├── locators/                # UI Element Selectors (separated by page)
├── pages/                   # Page Object classes (methods/actions for UI)
├── reports/                 # Output directory for test artifacts
│   ├── allure-results/      # Raw Allure data
│   ├── screenshots/         # Captured screenshots on failure
│   ├── traces/              # Playwright trace zips
│   └── videos/              # Video recordings of tests
├── testcases/               # Pytest test scripts
├── utils/                   # Helper functions
│   ├── config_reader.py     # Parses config.ini
│   ├── excel_data_reader.py # Data-driven testing helpers
│   ├── random_data.py       # Faker data generator
│   └── xlutils.py           # Core Excel read/write utility
├── .gitignore               # Ignored files/folders for git
├── conftest.py              # Pytest hooks, fixtures, and browser setup
├── pytest.ini               # Pytest default CLI options and markers
└── requirements.txt         # Python package dependencies
```

---

## ⚙️ Configuration
The core environment setup is maintained in `config/config.ini`:
```ini
[Environment]
base_url = https://www.saucedemo.com/
```
You can easily switch this URL when testing different environments (e.g., Staging vs. Production). Pytest default flags (like `--browser` or `--video` settings) are maintained in `pytest.ini`.
