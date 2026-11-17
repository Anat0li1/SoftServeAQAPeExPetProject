import time
from unittest import case

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

TEST_USERNAME = 'demo_user'
TEST_PASSWORD = 'Demo@123'
EXPECTED_COUNT = 12
NEEDED_PRODUCT = "Aurora Wireless Headphones"
BUTTON_TITLE = "Add to cart"
UPDATED_BUTTON_TITLE = "Remove"
PRICE_STYLE = "american"
FIXED_TAX = 0.08
FIRST_NAME = "Anna"
LAST_NAME = "Smith"
EMAIL = "anna@smith.com"
PHONE = "1231231233"
CITY = "New York"
STATE = "New York"
STREET_ADDRESS = "Famous Street, 14"
ZIP_CODE = "12345"
CVV = "123"
CARD_NUMBER = "4242 4242 4242 4242"
EXPIRY = "12/30"
CARD_NAME = "Main card"
EXPECTED_MESSAGE = "Thank you for your order!"
DEFAULT_PAYMENT_METHOD = "Card"
DEFAULT_DELIVERY = "Standard"
EXPECTED_ITEMS = 1
ORDER_START = "NS-"
DELIVERY_LABEL = "Delivery"
PAYMENT_LABEL = "Payment"

def retrieve_price(style, price):
    match style.lower():
        case "american":
            return float(price.strip(" $"))
        case _:
            return float(price)


def test_successful_product_buying():
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

        #driver.find_element(By.CSS_SELECTOR, "li[data-product-id='p1']")
        product_item = driver.find_element(By.XPATH, f"//a[text()='{NEEDED_PRODUCT}']/../..")
        product_button = driver.find_element(By.XPATH, f"//a[text()='{NEEDED_PRODUCT}']/../..//button")
        #product_button = product_item.find_element(By.XPATH, "//button")
        assert product_button.text == BUTTON_TITLE, f"Expected '{BUTTON_TITLE}' but got '{product_button.text}"
        product_button.click()
        assert product_button.text == UPDATED_BUTTON_TITLE, f"Expected '{UPDATED_BUTTON_TITLE}' but got '{product_button.text}"
        product_price = product_item.find_element(By.XPATH, "//span[@data-testid='product-price']").text

        cart_link_button = driver.find_element(By.CSS_SELECTOR, "a[data-testid='cart-link']")
        cart_link_button.click()
        time.sleep(2)

        cart_item = driver.find_elements(By.XPATH, "//li[@data-testid='cart-item']")[0]
        cart_item_prices = driver.find_elements(By.XPATH, "//div[contains(text(), '$')]")
        for cart_item_price in cart_item_prices:
            assert product_price in cart_item_price.text, f"Expected '{product_price}' but got '{cart_item_price.text}"

        order_summary_panel = driver.find_element(By.TAG_NAME, "aside")
        prices_box = order_summary_panel.find_element(By.TAG_NAME, "dl")
        subtotal_price = prices_box.find_element(By.XPATH, "//dt[text()='Subtotal']/following-sibling::dd").text
        assert product_price == subtotal_price, f"Expected '{subtotal_price}' but got '{product_price}'"
        shipping_price = prices_box.find_element(By.XPATH, "//dt[text()='Shipping']/following-sibling::dd").text
        general_price = retrieve_price(PRICE_STYLE, subtotal_price)
        if "Free" not in shipping_price.strip():
            general_price += retrieve_price(PRICE_STYLE, shipping_price)

        total_price = prices_box.find_element(By.XPATH, "//dt[text()='Total']/following-sibling::dd").text
        expectedCost = round(general_price * (1 + FIXED_TAX), 2)
        actualCost = retrieve_price(PRICE_STYLE, total_price)
        assert actualCost == expectedCost, f"Expected '{expectedCost}' but got '{actualCost}'"

        checkout_button = order_summary_panel.find_element(By.XPATH, "//a[@data-testid='checkout-button']")
        checkout_button.click()
        time.sleep(2)

        contact_and_shipping_panel = driver.find_element(By.XPATH, "//h2[contains(text(), 'Contact')]/..")
        contact_and_shipping_panel.find_element(By.ID, "first-name").send_keys(FIRST_NAME)
        contact_and_shipping_panel.find_element(By.ID, "last-name").send_keys(LAST_NAME)
        contact_and_shipping_panel.find_element(By.ID, "email").send_keys(EMAIL)
        contact_and_shipping_panel.find_element(By.ID, "phone").send_keys(PHONE)
        contact_and_shipping_panel.find_element(By.ID, "address").send_keys(STREET_ADDRESS)
        contact_and_shipping_panel.find_element(By.ID, "city").send_keys(CITY)
        Select(contact_and_shipping_panel.find_element(By.ID, "state")).select_by_value(STATE)
        contact_and_shipping_panel.find_element(By.ID, "zip").send_keys(ZIP_CODE)

        payment_panel = driver.find_element(By.XPATH, "//h2[contains(text(), 'Payment')]/..")
        payment_panel.find_element(By.ID, "card-name").send_keys(CARD_NAME)
        payment_panel.find_element(By.ID, "card-number").send_keys(CARD_NUMBER)
        payment_panel.find_element(By.ID, "card-expiry").send_keys(EXPIRY)
        payment_panel.find_element(By.ID, "card-cvv").send_keys(CVV)

        agree_terms_checkbox = driver.find_element(By.XPATH, "//input[@data-testid='accept-terms' or @type='checkbox']")
        agree_terms_checkbox.click()
        driver.find_element(By.XPATH, "//button[@data-testid='place-order' or @type='submit']").click()

        error_element = driver.find_elements(By.XPATH, "//div[@role='alert']")
        assert len(error_element) == 0, "Expected no error elements"

        time.sleep(5)
        successful_order_panel = driver.find_element(By.CSS_SELECTOR, "div[data-testid='order-success']")
        actual_message = successful_order_panel.find_element(By.TAG_NAME, "h1").text
        assert actual_message == EXPECTED_MESSAGE, f"Expected '{EXPECTED_MESSAGE}' but got '{actual_message}'"
        order_id = successful_order_panel.find_element(By.CSS_SELECTOR, "p[data-testid='order-id']").text
        assert order_id.startswith(ORDER_START), f"Expected order id starting with '{ORDER_START}' but got '{order_id}'"
        assert order_id.strip(ORDER_START).isdecimal(), f"Expected sequence after {ORDER_START} to be numeric"
        order_table = successful_order_panel.find_element(By.TAG_NAME, "dl")
        order_items_count = order_table.find_element(By.CSS_SELECTOR, "dd[data-testid='order-items']").text
        assert int(order_items_count) == EXPECTED_ITEMS, f"Expected '{EXPECTED_ITEMS}' but got '{order_items_count}'"

        order_item_delivery = successful_order_panel.find_elements(By.XPATH, f"//dt[text()='{DELIVERY_LABEL}']/following-sibling::dd")[0].text
        assert order_item_delivery == DEFAULT_DELIVERY, f"Expected '{DEFAULT_DELIVERY}' but got '{order_item_delivery}'"
        order_item_payment = successful_order_panel.find_elements(By.XPATH, f"//dt[text()='{PAYMENT_LABEL}']/following-sibling::dd")[0].text
        assert order_item_payment == DEFAULT_PAYMENT_METHOD, f"Expected '{DEFAULT_PAYMENT_METHOD}' but got '{order_item_payment}'"

        order_total = successful_order_panel.find_element(By.CSS_SELECTOR, "dd[data-testid='order-total']").text
        assert retrieve_price(PRICE_STYLE, order_total) == expectedCost, f"Expected '{expectedCost}' but got '{order_total}'"

    finally:
        driver.quit()