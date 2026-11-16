import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from datetime import datetime

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
DEFAULT_STATUS = "Processing"
ORDER_START = "NS-"
ORDER_COLUMN_NAME = "order"
ORDER_DATE_NAME = "date"
ORDER_ITEMS_NAME = "items"
ORDER_STATUS_NAME = "status"
ORDER_TOTAL_NAME = "total"
MAX_DIFF_SECONDS = 5



column_order_dict = {}

def retrieve_price(style, price):
    match style.lower():
        case "american":
            return float(price.strip(" $"))
        case _:
            return float(price)

def test_order_appearing_in_history():

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

        my_orders_button = driver.find_element(By.CSS_SELECTOR, "a[data-testid='orders-link']")
        products_button = driver.find_element(By.CSS_SELECTOR, "a[data-testid='nav-products']")
        my_orders_button.click()
        time.sleep(2)
        orders_table = driver.find_elements(By.TAG_NAME, "table")
        assert len(orders_table) == 0, f"Expected no order table on the page"
        old_rows_number = len(orders_table)
        products_button.click()

        product_item = driver.find_element(By.XPATH, f"//a[text()='{NEEDED_PRODUCT}']/../..")
        product_button = driver.find_element(By.XPATH, f"//a[text()='{NEEDED_PRODUCT}']/../..//button")
        product_button.click()
        product_price = product_item.find_element(By.XPATH, "//span[@data-testid='product-price']").text

        cart_link_button = driver.find_element(By.CSS_SELECTOR, "a[data-testid='cart-link']")
        cart_link_button.click()
        time.sleep(2)

        order_summary_panel = driver.find_element(By.TAG_NAME, "aside")
        prices_box = order_summary_panel.find_element(By.TAG_NAME, "dl")
        subtotal_price = prices_box.find_element(By.XPATH, "//dt[text()='Subtotal']/following-sibling::dd").text
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
        submission_time = datetime.now()

        time.sleep(3)

        successful_order_panel = driver.find_element(By.CSS_SELECTOR, "div[data-testid='order-success']")
        order_id = successful_order_panel.find_element(By.CSS_SELECTOR, "p[data-testid='order-id']").text
        view_orders_button = successful_order_panel.find_element(By.CSS_SELECTOR, "a[data-testid='view-orders']")
        view_orders_button.click()

        time.sleep(2)

        orders_table = driver.find_element(By.TAG_NAME, "table")
        headers = orders_table.find_elements(By.CSS_SELECTOR, "thead tr th")
        for i in range(1, len(headers) + 1):
            column_order_dict[headers[i - 1].text.lower()] = i
        all_rows = orders_table.find_elements(By.CSS_SELECTOR, "tr[data-testid='order-row']")
        new_rows_number = len(all_rows)
        assert new_rows_number == old_rows_number + 1, (f"Expected new table rows '{new_rows_number}' "
                                                        f"to be 1 row more than old ones'{old_rows_number}'")

        last_added_row = all_rows[0]
        row_order_id = last_added_row.find_element(By.XPATH, f"//td[{column_order_dict[ORDER_COLUMN_NAME]}]").text
        assert row_order_id == order_id, f"Expected '{order_id}' but got '{row_order_id}'"
        row_order_date = last_added_row.find_element(By.XPATH, f"//td[{column_order_dict[ORDER_DATE_NAME]}]").text
        order_time = datetime.strptime(row_order_date.strip(), "%d.%m.%Y, %H:%M:%S")
        diff_seconds = abs((order_time - submission_time).total_seconds())
        assert diff_seconds < MAX_DIFF_SECONDS, (f"Expected order time'{order_time}' not to differ from"
                                                 f"submission time '{submission_time}' more than {MAX_DIFF_SECONDS}s")

        row_order_items = int(last_added_row.find_element(By.XPATH, f"//td[{column_order_dict[ORDER_ITEMS_NAME]}]").text)
        assert row_order_items == EXPECTED_ITEMS, f"Expected '{EXPECTED_ITEMS}' but got '{row_order_items}'"
        row_order_status = last_added_row.find_element(By.CSS_SELECTOR, "td span").text
        assert row_order_status == DEFAULT_STATUS, f"Expected '{DEFAULT_STATUS}' but got '{row_order_status}'"
        row_order_price = last_added_row.find_element(By.XPATH, f"//td[{column_order_dict[ORDER_TOTAL_NAME]}]").text
        actual_order_price = retrieve_price(PRICE_STYLE, row_order_price)
        assert actualCost == actual_order_price, f"Expected '{actual_order_price}' but got '{total_price}'"



    finally:
        driver.quit()