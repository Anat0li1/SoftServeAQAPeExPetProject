from pages.login_page import LoginPage
from utils.price_utils import PriceUtils

TEST_USERNAME = 'demo_user'
TEST_PASSWORD = 'Demo@123'

SORT_BY_VALUE = "price-asc"
PRICE_STYLE = "american"

BASE_URL = "https://www.practiceqaautomation.com/shop"


def test_sorting_products_by_price(driver):
    driver.get(BASE_URL)

    login_page = LoginPage(driver)
    price_utils = PriceUtils(PRICE_STYLE)
    products_page = login_page.login(TEST_USERNAME, TEST_PASSWORD)

    products_page.sort_products(SORT_BY_VALUE)

    sorted_prices = products_page.get_product_prices()

    for i in range(len(sorted_prices) - 1):
        previous_price = price_utils.retrieve_price(sorted_prices[i])
        next_price = price_utils.retrieve_price(sorted_prices[i + 1])

        assert previous_price <= next_price, (
            f"In ascending order previous cost must be <= to the next cost, "
            f"but the cost of product {i} is higher than product {i + 1} "
            f"({previous_price} > {next_price})"
        )
