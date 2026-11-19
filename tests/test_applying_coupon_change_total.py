from pages.login_page import LoginPage
from utils.price_utils import PriceUtils

TEST_USERNAME = 'demo_user'
TEST_PASSWORD = 'Demo@123'
NEEDED_PRODUCT = "Aurora Wireless Headphones"

PRICE_STYLE = "american"
FIXED_TAX = 0.08
PROMO_CODE = "SAVE10"
EXPECTED_PROMO_DISCOUNT = 0.1
PROMO_MESSAGE = "SAVE10 applied — 10% off your order"

BASE_URL = "https://www.practiceqaautomation.com/shop"


def test_applying_coupon_change_total(driver):
    driver.get(BASE_URL)
    price_utils = PriceUtils(PRICE_STYLE)

    login_page = LoginPage(driver)
    products_page = login_page.login(TEST_USERNAME, TEST_PASSWORD)

    product = products_page.get_product(NEEDED_PRODUCT)
    product_price = product.get_price()

    product.click_button()

    cart_page = products_page.open_cart()
    order_summary = cart_page.get_order_summary()

    cart_item_prices = cart_page.get_cart_item_prices()

    for cart_item_price in cart_item_prices:
        assert product_price in cart_item_price, \
            f"Expected '{product_price}' but got '{cart_item_price}'"

    order_summary.apply_coupon(PROMO_CODE)

    actual_promo_message = order_summary.get_coupon_message()
    assert actual_promo_message == PROMO_MESSAGE, \
        f"Expected '{PROMO_MESSAGE}' but got '{actual_promo_message}'"

    subtotal_price = order_summary.get_subtotal()
    assert product_price == subtotal_price, \
        f"Expected '{product_price}' but got '{subtotal_price}'"

    discount = order_summary.get_discount()

    expected_discount = round(
        EXPECTED_PROMO_DISCOUNT * price_utils.retrieve_price(subtotal_price), 2
    )
    actual_discount = price_utils.retrieve_price(discount)

    assert actual_discount < 0, "Discount should be lower than 0"
    assert abs(actual_discount) == expected_discount, \
        f"Expected '{expected_discount}' but got '{actual_discount}'"

    shipping_price = order_summary.get_shipping()

    general_price = (price_utils.retrieve_price(subtotal_price)
                     + actual_discount)

    if "Free" not in shipping_price.strip():
        general_price += price_utils.retrieve_price(shipping_price)

    total_price = order_summary.get_total()

    expected_cost = round(general_price * (1 + FIXED_TAX), 2)
    actual_cost = price_utils.retrieve_price(total_price)

    assert actual_cost == expected_cost, \
        f"Expected '{expected_cost}' but got '{actual_cost}'"
