import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

TEST_USERNAME = 'demo_user'
TEST_PASSWORD = 'Demo@123'
TOTAL_COUNT = 12
COUNT_AFTER_SEARCH = 1
SEARCH_WORD = "headphones"


def test_searching_by_product_name():
    chrome_options = Options()

    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    }
    chrome_options.add_experimental_option("prefs", prefs)

    chrome_options.add_argument(
        "--disable-features=PasswordLeakDetection,PasswordManagerLeakDetection,AutofillServerCommunication"
    )
    chrome_options.add_argument("--disable-save-password-bubble")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get("https://www.practiceqaautomation.com/shop")
        assert "Nova Shop: E-commerce Practice App" in driver.title
        driver.maximize_window()
        driver.find_element(By.ID, "username").send_keys(TEST_USERNAME)
        driver.find_element(By.ID, "password").send_keys(TEST_PASSWORD)
        driver.find_element(By.CSS_SELECTOR, "button[data-testid='login-button'], button[type='submit']").click()

        time.sleep(2)
        total_items = driver.find_elements(By.CSS_SELECTOR, "li[data-testid='product-card']")
        assert len(total_items) == TOTAL_COUNT, f"Expected {TOTAL_COUNT} items, got {len(total_items)}"
        showing_text = driver.find_element(By.XPATH, "//p[@data-testid='product-count']").text
        assert showing_text == f"Showing {TOTAL_COUNT} of {TOTAL_COUNT} products", f""

        found_products = 0
        product_names = driver.find_elements(By.CSS_SELECTOR, "a[data-testid='product-name']")
        for product_name in product_names:
            if SEARCH_WORD in product_name.text.lower():
                found_products += 1
        assert found_products == COUNT_AFTER_SEARCH, f"Expected {COUNT_AFTER_SEARCH} items, got {found_products}"

        searching_field = driver.find_element(By.CSS_SELECTOR, "input[data-testid='search-input']")
        searching_field.send_keys(SEARCH_WORD)
        time.sleep(1)

        total_items_after_search = driver.find_elements(By.CSS_SELECTOR, "li[data-testid='product-card']")
        assert len(total_items_after_search) == COUNT_AFTER_SEARCH, f"Expected {COUNT_AFTER_SEARCH} items, got {len(total_items)}"
        showing_text = driver.find_element(By.XPATH, "//p[@data-testid='product-count']").text
        assert showing_text == f"Showing {COUNT_AFTER_SEARCH} of {TOTAL_COUNT} products", f""
    finally:
        driver.quit()