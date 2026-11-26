from pages.login_page import LoginPage
from utils.price_utils import PriceUtils


def test_applying_coupon_change_total(driver, config):
    driver.get(config.BASE_URL)
    price_utils = PriceUtils(config.PRICE_STYLE)

    login_page = LoginPage(driver)
    products_page = login_page.login(config.TEST_USERNAME,
                                     config.TEST_PASSWORD)

    product = products_page.get_product(config.NEEDED_PRODUCT)
    product_price = product.get_price()

    product.click_button()

    cart_page = products_page.open_cart()
    order_summary = cart_page.get_order_summary()

    cart_item_prices = cart_page.get_cart_item_prices()

    for cart_item_price in cart_item_prices:
        assert product_price in cart_item_price, \
            f"Expected '{product_price}' but got '{cart_item_price}'"

    order_summary.apply_coupon(config.PROMO_CODE)

    actual_promo_message = order_summary.get_coupon_message()
    assert actual_promo_message == config.PROMO_MESSAGE, \
        f"Expected '{config.PROMO_MESSAGE}' but got '{actual_promo_message}'"

    subtotal_price = order_summary.get_subtotal()
    assert product_price == subtotal_price, \
        f"Expected '{product_price}' but got '{subtotal_price}'"

    discount = order_summary.get_discount()

    expected_discount = round(
        config.EXPECTED_PROMO_DISCOUNT * price_utils.retrieve_price(subtotal_price), 2
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

    expected_cost = round(general_price * (1 + config.FIXED_TAX), 2)
    actual_cost = price_utils.retrieve_price(total_price)

    assert actual_cost == expected_cost, \
        f"Expected '{expected_cost}' but got '{actual_cost}'"
