import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

TEST_USERNAME = 'demo_user'
TEST_PASSWORD = 'Demo@123'
SORT_BY_VALUE = "price-asc"
PRICE_STYLE = "american"

def retrieve_price(style, price):
    price = price.replace("−", "-").replace("–", "-")
    match style.lower():
        case "american":
            if price.startswith("-"):
                return -float(price.strip(" -$"))
            return float(price.strip(" $"))
        case _:
            return float(price)

def test_sorting_products_by_price():

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
        driver.maximize_window()
        driver.find_element(By.ID, "username").send_keys(TEST_USERNAME)
        driver.find_element(By.ID, "password").send_keys(TEST_PASSWORD)
        driver.find_element(By.CSS_SELECTOR, "button[data-testid='login-button'], button[type='submit']").click()


        time.sleep(2)

        sorting_select = Select(driver.find_element(By.CSS_SELECTOR, "select[data-testid='sort-select'"))
        sorting_select.select_by_value(SORT_BY_VALUE)

        time.sleep(1)

        sorted_prices = driver.find_elements(By.CSS_SELECTOR, "span[data-testid='product-price']")
        for i in range(len(sorted_prices) - 1):
            previous_price = retrieve_price(PRICE_STYLE, sorted_prices[i].text)
            next_price = retrieve_price(PRICE_STYLE, sorted_prices[i + 1].text)
            assert previous_price <= next_price, (f"In ascending order previous cost must be <= to the next cost, but the cost "
                                                  f"of the product {i} is higher than the cost of the product {i+1} "
                                                  f"({previous_price} > {next_price})")

    finally:
        driver.quit()