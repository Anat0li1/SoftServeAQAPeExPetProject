import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

TEST_USERNAME = 'demo_user'
TEST_PASSWORD = 'Demo@123'
EXPECTED_COUNT = 12
NEEDED_PRODUCT = "Aurora Wireless Headphones"
PRICE_STYLE = "american"
FIXED_TAX = 0.08
PROMO_CODE = "SAVE10"
EXPECTED_PROMO_DISCOUNT = 0.1
PROMO_MESSAGE = "SAVE10 applied — 10% off your order"

def retrieve_price(style, price):
    price = price.replace("−", "-").replace("–", "-")
    match style.lower():
        case "american":
            if price.startswith("-"):
                return -float(price.strip(" -$"))
            return float(price.strip(" $"))
        case _:
            return float(price)

def test_applying_coupon_change_total():
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

        product_item = driver.find_element(By.XPATH, f"//a[text()='{NEEDED_PRODUCT}']/../..")
        product_button = driver.find_element(By.XPATH, f"//a[text()='{NEEDED_PRODUCT}']/../..//button")
        product_button.click()
        product_price = product_item.find_element(By.XPATH, "//span[@data-testid='product-price']").text

        cart_link_button = driver.find_element(By.CSS_SELECTOR, "a[data-testid='cart-link']")
        cart_link_button.click()
        time.sleep(2)

        cart_item = driver.find_elements(By.XPATH, "//li[@data-testid='cart-item']")[0]
        cart_item_prices = driver.find_elements(By.XPATH, "//div[contains(text(), '$')]")
        for cart_item_price in cart_item_prices:
            assert product_price in cart_item_price.text, f"Expected '{product_price}' but got '{cart_item_price.text}"



        order_summary_panel = driver.find_element(By.TAG_NAME, "aside")
        order_summary_panel.find_element(By.CSS_SELECTOR, "input[data-testid='coupon-input']").send_keys(PROMO_CODE)
        order_summary_panel.find_element(By.CSS_SELECTOR, "button[data-testid='apply-coupon']").click()
        time.sleep(1)

        promo_message = order_summary_panel.find_element(By.CSS_SELECTOR, "p[data-testid='coupon-message']").text
        assert promo_message == PROMO_MESSAGE, f"Expected '{PROMO_MESSAGE}' but got '{promo_message}'"

        prices_box = order_summary_panel.find_element(By.TAG_NAME, "dl")
        subtotal_price = prices_box.find_element(By.XPATH, "//dt[text()='Subtotal']/following-sibling::dd").text
        assert product_price == subtotal_price, f"Expected '{subtotal_price}' but got '{product_price}'"
        discount = prices_box.find_element(By.XPATH, "//dt[contains(text(), 'Discount')]/following-sibling::dd").text
        expected_discount = round(EXPECTED_PROMO_DISCOUNT * retrieve_price(PRICE_STYLE, subtotal_price), 2)
        actual_discount = retrieve_price(PRICE_STYLE, discount)
        assert actual_discount < 0, "Discount should be lower than 0"
        assert abs(actual_discount) == expected_discount, f"Expected '{expected_discount}' but got '{actual_discount}'"

        shipping_price = prices_box.find_element(By.XPATH, "//dt[text()='Shipping']/following-sibling::dd").text
        general_price = retrieve_price(PRICE_STYLE, subtotal_price) + actual_discount
        if "Free" not in shipping_price.strip():
            general_price += retrieve_price(PRICE_STYLE, shipping_price)

        total_price = prices_box.find_element(By.XPATH, "//dt[text()='Total']/following-sibling::dd").text
        expectedCost = round(general_price * (1 + FIXED_TAX), 2)
        actualCost = retrieve_price(PRICE_STYLE, total_price)
        assert actualCost == expectedCost, f"Expected '{expectedCost}' but got '{actualCost}'"


    finally:
        driver.quit()