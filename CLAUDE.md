# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Playwright + Pytest end-to-end test automation for the GoSystem tax filing web application. Tests automate login, tax return creation, data entry, and computation workflows.

## Setup & Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Run all tests
pytest

# Run with Allure reporting
pytest --alluredir=allure-results -v

# Run a single test file
pytest testcases/LoginTest.py -v

# Run a single test function
pytest testcases/LoginTest.py::TestLogin::test_login -v

# Run in headed mode (CI)
HEADLESS=false pytest --alluredir=allure-results -v --tb=short
```

## Architecture

**Layer structure:**

1. **testcases/** — Test files (`*Test.py`) + `conftest.py` fixtures
2. **pages/** — Page Object Model classes
3. **utilities/** — Config reader, Excel data provider, logging
4. **ConfigurationData/conf.ini** — All URLs and CSS/XPath locators
5. **exceldata/** — Test data Excel files (gitignored; samples provided)

**Page Object hierarchy:**
- `BasePage` — 40+ reusable Playwright wrapper methods (click, type, verify, dropdown, tab management, etc.)
- `LoginPage`, `HomePage`/`CreateNewReturn`, `ReturnsPage`, `EnterDetailsPage` — all extend `BasePage`

**Test fixtures (conftest.py):**
- `browser` and `page` are **session-scoped** — all tests share one browser instance
- `setup_function` navigates to the configured URL before each test
- `capture_screenshot_on_failure` attaches screenshots to Allure on failure
- `HEADLESS` env var controls headless mode

**Test execution order:**
- `LoginTest.py` must run before `CreateReturnTest.py`
- Enforced via `@pytest.mark.dependency(name="login")` / `depends=["login"]`
- Tests are parametrized over rows from Excel files

## Test Data

- `exceldata/testdata.xlsx` (gitignored) — Login credentials: `LoginID`, `Firm`, `Location`, `Password`
- `exceldata/ReturnDetails.xlsx` (gitignored) — Return data; `Locator` column is written back during test execution
- Sample files: `testdata_sample.xlsx`, `ReturnDetails_sample.xlsx`

## Locators

All CSS/XPath selectors are centralized in `ConfigurationData/conf.ini` under `[locators]`. Add new locators there and read them via `utilities/configReader.py`, not hardcoded in page classes.

## Custom Dropdown Handling

The GoSystem app uses `<saf-select>` web components that require custom handling via `BasePage.select_custom_dropdown()`. Standard `<select>` elements use `select_dropdown_by_value()` or `select_dropdown_by_label()`.

## CI/CD

Jenkins pipeline defined in `Jenkinsfile`:
1. Checkout → 2. Setup venv → 3. Install Playwright → 4. Run tests
- Publishes Allure reports and archives screenshots as artifacts
- Uses `HEADLESS=false` in CI environment