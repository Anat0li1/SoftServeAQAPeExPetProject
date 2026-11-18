from pages.login_page import LoginPage
from utils.json_reader import JSONReader
from utils.price_utils import PriceUtils

TEST_USERNAME = 'demo_user'
TEST_PASSWORD = 'Demo@123'

NEEDED_PRODUCT = "Aurora Wireless Headphones"

BUTTON_TITLE = "Add to cart"
UPDATED_BUTTON_TITLE = "Remove"

PRICE_STYLE = "american"
FIXED_TAX = 0.08

EXPECTED_MESSAGE = "Thank you for your order!"
DEFAULT_PAYMENT_METHOD = "Card"
DEFAULT_DELIVERY = "Standard"

EXPECTED_ITEMS = 1
ORDER_START = "NS-"

DELIVERY_LABEL = "Delivery"
PAYMENT_LABEL = "Payment"

BASE_URL = "https://www.practiceqaautomation.com/shop"


def test_successful_product_buying(driver):
    driver.get(BASE_URL)

    login_page = LoginPage(driver)
    price_utils = PriceUtils(PRICE_STYLE)
    json_reader = JSONReader("./../test_data/order_data.json")
    products_page = login_page.login(TEST_USERNAME, TEST_PASSWORD)

    product = products_page.get_product(NEEDED_PRODUCT)
    actual_button_title = product.get_button_text()
    assert actual_button_title == BUTTON_TITLE, \
        f"Expected '{BUTTON_TITLE}' but got '{actual_button_title}'"

    product_price = product.get_price()
    product.click_button()

    updated_button_title = product.get_button_text()
    assert updated_button_title == UPDATED_BUTTON_TITLE, \
        f"Expected '{UPDATED_BUTTON_TITLE}' but got '{updated_button_title}'"

    cart_page = products_page.open_cart()
    cart_item_prices = cart_page.get_cart_item_prices()
    for cart_item_price in cart_item_prices:
        assert product_price in cart_item_price, \
            f"Expected '{product_price}' but got '{cart_item_price}'"

    order_summary = cart_page.get_order_summary()
    subtotal_price = order_summary.get_subtotal()
    assert product_price == subtotal_price, \
        f"Expected '{product_price}' but got '{subtotal_price}'"

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
    order_data = json_reader.load_test_data()
    checkout_page.get_contact_form().fill(order_data["contact_form_data"])
    checkout_page.get_payment_form().fill(order_data["payment_form_data"])
    confirmation_page = checkout_page.place_order()

    actual_errors = checkout_page.get_errors()
    assert len(actual_errors) == 0, "Expected no error elements"

    confirmation_panel = confirmation_page.get_success_panel()
    actual_message = confirmation_panel.get_title()
    assert actual_message == EXPECTED_MESSAGE, \
        f"Expected '{EXPECTED_MESSAGE}' but got '{actual_message}'"

    order_id = confirmation_panel.get_order_id()
    assert order_id.startswith(ORDER_START), \
        f"Expected order ID starting with '{ORDER_START}' but got '{order_id}'"
    assert order_id[len(ORDER_START):].isdecimal(), \
        f"Expected numeric sequence after '{ORDER_START}'"

    order_items_count = confirmation_panel.get_items_count()
    assert int(order_items_count) == EXPECTED_ITEMS, \
        f"Expected '{EXPECTED_ITEMS}' but got '{order_items_count}'"

    order_item_delivery = confirmation_panel.get_delivery(DELIVERY_LABEL)
    assert order_item_delivery == DEFAULT_DELIVERY, \
        f"Expected '{DEFAULT_DELIVERY}' but got '{order_item_delivery}'"

    order_item_payment = confirmation_panel.get_payment(PAYMENT_LABEL)
    assert order_item_payment == DEFAULT_PAYMENT_METHOD, \
        f"Expected '{DEFAULT_PAYMENT_METHOD}' but got '{order_item_payment}'"

    order_total = confirmation_panel.get_total()
    assert price_utils.retrieve_price(order_total) == expected_cost, \
        f"Expected '{expected_cost}' but got '{order_total}'"
