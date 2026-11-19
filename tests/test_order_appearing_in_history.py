from datetime import datetime

from pages.login_page import LoginPage
from utils.price_utils import PriceUtils

TEST_USERNAME = 'demo_user'
TEST_PASSWORD = 'Demo@123'

NEEDED_PRODUCT = "Aurora Wireless Headphones"

PRICE_STYLE = "american"
FIXED_TAX = 0.08

contact_form_data = {
    "first_name" : "Anna",
    "last_name" : "Smith",
    "email" : "anna@smith.com",
    "phone" : "1231231233",
    "city" : "New York",
    "state" : "New York",
    "address" : "Famous Street, 14",
    "zip" : "12345",
}

payment_form_data = {
    "card_name": "Main card",
    "card_number": "4242 4242 4242 4242",
    "expiry": "12/30",
    "cvv": "123",
}

DEFAULT_STATUS = "Processing"
EXPECTED_ITEMS = 1

ORDER_COLUMN_NAME = "order"
ORDER_DATE_NAME = "date"
ORDER_ITEMS_NAME = "items"
ORDER_STATUS_NAME = "status"
ORDER_TOTAL_NAME = "total"

MAX_DIFF_SECONDS = 5

BASE_URL = "https://www.practiceqaautomation.com/shop"


def test_order_appearing_in_history(driver):
    driver.get(BASE_URL)

    login_page = LoginPage(driver)
    price_utils = PriceUtils(PRICE_STYLE)
    products_page = login_page.login(TEST_USERNAME, TEST_PASSWORD)

    orders_page = products_page.open_orders()

    old_rows_number = 0
    if not orders_page.is_invisible(orders_page.ORDERS_TABLE):
        old_rows_number = len(orders_page.get_order_rows())
    assert old_rows_number == 0, "Expected no orders in history"

    products_page.open_products()
    product = products_page.get_product(NEEDED_PRODUCT)
    product.click_button()

    cart_page = products_page.open_cart()
    order_summary = cart_page.get_order_summary()

    subtotal_price = order_summary.get_subtotal()
    shipping_price = order_summary.get_shipping()

    general_price = price_utils.retrieve_price(subtotal_price)
    if "Free" not in shipping_price.strip():
        general_price += price_utils.retrieve_price(shipping_price)
    total_price = order_summary.get_total()

    expected_cost = round(general_price * (1 + FIXED_TAX), 2)
    actual_cost = price_utils.retrieve_price(total_price)
    assert actual_cost == expected_cost, \
        f"Expected '{expected_cost}' but got '{actual_cost}'"

    checkout_page = cart_page.open_checkout()
    checkout_page.get_contact_form().fill(contact_form_data)
    checkout_page.get_payment_form().fill(payment_form_data)

    submission_time = datetime.now()
    confirmation_page = checkout_page.place_order()

    order_id = confirmation_page.get_success_panel().get_order_id()
    orders_page = confirmation_page.get_success_panel().open_orders()
    all_rows = orders_page.get_order_rows()
    assert len(all_rows) == old_rows_number + 1, \
        f"Expected {old_rows_number + 1} rows, got {len(all_rows)}"

    last_added_row = all_rows[0]
    row_order_id = orders_page.get_cell_value(
        last_added_row, ORDER_COLUMN_NAME
    )
    assert row_order_id == order_id, \
        f"Expected '{order_id}' but got '{row_order_id}'"

    row_order_date = orders_page.get_cell_value(
        last_added_row, ORDER_DATE_NAME
    )
    order_time = datetime.strptime(
        row_order_date.strip(), "%d.%m.%Y, %H:%M:%S"
    )
    diff_seconds = abs((order_time - submission_time).total_seconds())
    assert diff_seconds < MAX_DIFF_SECONDS, \
        f"Order time differs from submission time by {diff_seconds} seconds"

    row_order_items = int(
        orders_page.get_cell_value(last_added_row, ORDER_ITEMS_NAME)
    )
    assert row_order_items == EXPECTED_ITEMS, \
        f"Expected '{EXPECTED_ITEMS}' but got '{row_order_items}'"

    row_order_status = orders_page.get_order_status(last_added_row)
    assert row_order_status == DEFAULT_STATUS, \
        f"Expected '{DEFAULT_STATUS}' but got '{row_order_status}'"

    row_order_price = orders_page.get_cell_value(
        last_added_row, ORDER_TOTAL_NAME
    )
    actual_order_price = price_utils.retrieve_price(row_order_price)
    assert actual_cost == actual_order_price, \
        f"Expected '{actual_cost}' but got '{actual_order_price}'"
