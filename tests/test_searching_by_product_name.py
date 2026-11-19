import pytest

from pages.login_page import LoginPage

TEST_USERNAME = 'demo_user'
TEST_PASSWORD = 'Demo@123'
TOTAL_COUNT = 12
COUNT_AFTER_SEARCH = 1
SEARCH_WORD = "headphones"
ANOTHER_SEARCH_WORD = "ni"
ANOTHER_COUNT_AFTER_SEARCH = 4
BASE_URL = "https://www.practiceqaautomation.com/shop"
EXPECTED_SHOW_TEXT = "Showing {0} of {1} products"

@pytest.mark.parametrize("goods_name, expected_count", [
    (SEARCH_WORD, COUNT_AFTER_SEARCH),
    (ANOTHER_SEARCH_WORD, ANOTHER_COUNT_AFTER_SEARCH)
])
def test_searching_by_product_name(driver, goods_name, expected_count):
    driver.get(BASE_URL)

    login_page = LoginPage(driver)

    products_page = login_page.login(TEST_USERNAME, TEST_PASSWORD)
    start_count = products_page.get_products_count()
    assert start_count == TOTAL_COUNT, \
        f"Expected {TOTAL_COUNT} items, got {start_count}"
    showing_text = products_page.get_product_count_text()
    expected_start_show_text = EXPECTED_SHOW_TEXT.format(TOTAL_COUNT,
                                                         TOTAL_COUNT)
    assert showing_text == expected_start_show_text, \
        f"Expected {expected_start_show_text}, got {showing_text}"

    found_products = 0
    product_names = products_page.get_product_names()
    for product_name in product_names:
        if goods_name in product_name.lower():
            found_products += 1
    assert found_products == expected_count, \
        f"Expected {expected_count} items, got {found_products}"

    products_page.search_product(goods_name)

    finish_count = products_page.get_products_count()
    assert finish_count == expected_count, \
        f"Expected {expected_count} items, got {finish_count}"
    showing_text = products_page.get_product_count_text()
    expected_finish_show_text = EXPECTED_SHOW_TEXT.format(expected_count,
                                                          TOTAL_COUNT)
    assert showing_text == expected_finish_show_text, \
        f"Expected {expected_finish_show_text}, got {showing_text}"
