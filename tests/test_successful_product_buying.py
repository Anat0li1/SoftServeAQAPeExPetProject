from pages.login_page import LoginPage
from utils.json_reader import JSONReader
from utils.price_utils import PriceUtils


def test_successful_product_buying(driver, config):
    driver.get(config.BASE_URL)

    login_page = LoginPage(driver)
    price_utils = PriceUtils(config.PRICE_STYLE)
    json_reader = JSONReader(config.ORDER_DATA_FILE)
    products_page = login_page.login(config.TEST_USERNAME, config.TEST_PASSWORD)

    product = products_page.get_product(config.NEEDED_PRODUCT)
    actual_button_title = product.get_button_text()
    assert actual_button_title == config.BUTTON_TITLE, \
        f"Expected '{config.BUTTON_TITLE}' but got '{actual_button_title}'"

    product_price = product.get_price()
    product.click_button()

    updated_button_title = product.get_button_text()
    assert updated_button_title == config.UPDATED_BUTTON_TITLE, \
        f"Expected '{config.UPDATED_BUTTON_TITLE}' but got '{updated_button_title}'"

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

    expected_cost = round(general_price * (1 + config.FIXED_TAX), 2)
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
    assert actual_message == config.EXPECTED_MESSAGE, \
        f"Expected '{config.EXPECTED_MESSAGE}' but got '{actual_message}'"

    order_id = confirmation_panel.get_order_id()
    assert order_id.startswith(config.ORDER_START), \
        f"Expected order ID starting with '{config.ORDER_START}' but got '{order_id}'"
    assert order_id[len(config.ORDER_START):].isdecimal(), \
        f"Expected numeric sequence after '{config.ORDER_START}'"

    order_items_count = confirmation_panel.get_items_count()
    assert int(order_items_count) == config.EXPECTED_ITEMS, \
        f"Expected '{config.EXPECTED_ITEMS}' but got '{order_items_count}'"

    order_item_delivery = confirmation_panel.get_delivery(config.DELIVERY_LABEL)
    assert order_item_delivery == config.DEFAULT_DELIVERY, \
        f"Expected '{config.DEFAULT_DELIVERY}' but got '{order_item_delivery}'"

    order_item_payment = confirmation_panel.get_payment(config.PAYMENT_LABEL)
    assert order_item_payment == config.DEFAULT_PAYMENT_METHOD, \
        f"Expected '{config.DEFAULT_PAYMENT_METHOD}' but got '{order_item_payment}'"

    order_total = confirmation_panel.get_total()
    assert price_utils.retrieve_price(order_total) == expected_cost, \
        f"Expected '{expected_cost}' but got '{order_total}'"
