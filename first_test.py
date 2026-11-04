import time

from selenium import webdriver
from selenium.webdriver.common.by import By

TEST_USERNAME = 'demo_user'
TEST_PASSWORD = 'Demo@123'
EXPECTED_COUNT = 12

driver = webdriver.Chrome()
driver.get("https://www.practiceqaautomation.com/shop")
assert "Nova Shop: E-commerce Practice App" in driver.title
driver.maximize_window()
driver.find_element(By.ID, "username").send_keys(TEST_USERNAME)
driver.find_element(By.ID, "password").send_keys(TEST_PASSWORD)
driver.find_element(By.CSS_SELECTOR, "button[data-testid='login-button'], button[type='submit']").click()

time.sleep(2)
greeting_text = driver.find_element(By.CSS_SELECTOR, "span[data-testid='user-greeting']").text
assert greeting_text == f"Hi, {TEST_USERNAME}", f"Expected 'Hi, {TEST_USERNAME}', got '{greeting_text}'"
total_items = driver.find_elements(By.CSS_SELECTOR, "li[data-testid='product-card']")
assert len(total_items) == EXPECTED_COUNT, f"Expected {EXPECTED_COUNT} items, got {len(total_items)}"
showing_text = driver.find_element(By.XPATH, "//p[@data-testid='product-count']").text
assert showing_text == f"Showing {EXPECTED_COUNT} of {EXPECTED_COUNT} products", f""
