from pages.login_page import LoginPage
from utils.price_utils import PriceUtils


def test_sorting_products_by_price(driver, config):
    driver.get(config.BASE_URL)

    login_page = LoginPage(driver)
    price_utils = PriceUtils(config.PRICE_STYLE)
    products_page = login_page.login(config.TEST_USERNAME, config.TEST_PASSWORD)

    products_page.sort_products(config.SORT_BY_VALUE)

    sorted_prices = products_page.get_product_prices()

    for i in range(len(sorted_prices) - 1):
        previous_price = price_utils.retrieve_price(sorted_prices[i])
        next_price = price_utils.retrieve_price(sorted_prices[i + 1])

        assert previous_price <= next_price, (
            f"In ascending order previous cost must be <= to the next cost, "
            f"but the cost of product {i} is higher than product {i + 1} "
            f"({previous_price} > {next_price})"
        )
