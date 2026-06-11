"""
Selenium-based functional (UI) tests for the deployed Simple Calculator web app.

The target URL is read from the APP_URL environment variable (set by the pipeline to the
deployed Azure Web App). These tests drive a real browser (headless Chromium) against the
running application, verifying end-to-end behavior rather than individual functions.
"""
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

APP_URL = os.environ.get("APP_URL", "http://localhost:80")


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    drv = webdriver.Chrome(options=options)
    drv.implicitly_wait(10)
    yield drv
    drv.quit()


def _calculate(driver, a, op, b):
    driver.get(APP_URL)
    driver.find_element(By.NAME, "a").send_keys(str(a))
    driver.find_element(By.NAME, "b").send_keys(str(b))
    Select(driver.find_element(By.NAME, "op")).select_by_value(op)
    driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
    return driver.page_source


def test_homepage_loads(driver):
    driver.get(APP_URL)
    assert "Simple Calculator" in driver.page_source


def test_addition(driver):
    page = _calculate(driver, 4, "+", 5)
    assert "Result" in page
    assert "9" in page


def test_division_by_zero_shows_error(driver):
    page = _calculate(driver, 10, "/", 0)
    assert "Error" in page
    assert "Division by zero is not allowed" in page
