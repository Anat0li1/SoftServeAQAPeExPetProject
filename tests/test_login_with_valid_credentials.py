
from selenium import webdriver

from pages.login_page import LoginPage

TEST_USERNAME = 'demo_user'
TEST_PASSWORD = 'Demo@123'
EXPECTED_COUNT = 12
EXPECTED_TITLE = "Nova Shop: E-commerce Practice App"
EXPECTED_GREETING = f"Hi, {TEST_USERNAME}"
EXPECTED_SHOWING_TEXT = f"Showing {EXPECTED_COUNT} of {EXPECTED_COUNT} products"
BASE_URL = "https://www.practiceqaautomation.com/shop"


def test_login_with_valid_credentials(driver):
    driver.get(BASE_URL)

    login_page = LoginPage(driver)
    assert EXPECTED_TITLE in login_page.get_title(), f"Expected {EXPECTED_TITLE} in the page title"

    products_page = login_page.login(TEST_USERNAME, TEST_PASSWORD)
    actual_greeting = products_page.get_greetings_text()
    assert actual_greeting == EXPECTED_GREETING, f"Expected '{EXPECTED_GREETING}', got '{actual_greeting}'"
    total_items = products_page.get_products_count()
    assert total_items == EXPECTED_COUNT, f"Expected {EXPECTED_COUNT} items, got {total_items}"
    actual_showing_text = products_page.get_showing_text()
    assert actual_showing_text == EXPECTED_SHOWING_TEXT, f"Expected '{EXPECTED_SHOWING_TEXT}', got '{actual_showing_text}'"

    driver.quit()
