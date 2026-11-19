import pytest

from pages.login_page import LoginPage


@pytest.mark.parametrize("search_case", ["headphones", "ni"])
def test_searching_by_product_name(driver, config, search_case):
    search_data = {
        "headphones": (config.SEARCH_WORD,
                       config.COUNT_AFTER_SEARCH),
        "ni": (config.ANOTHER_SEARCH_WORD,
               config.ANOTHER_COUNT_AFTER_SEARCH),
    }
    goods_name, expected_count = search_data[search_case]
    driver.get(config.BASE_URL)

    login_page = LoginPage(driver)

    products_page = login_page.login(config.TEST_USERNAME,
                                     config.TEST_PASSWORD)
    start_count = products_page.get_products_count()
    assert start_count == config.EXPECTED_TOTAL_COUNT, \
        f"Expected {config.EXPECTED_TOTAL_COUNT} items, got {start_count}"
    showing_text = products_page.get_product_count_text()
    expected_start_show_text = config.EXPECTED_SHOW_TEXT.format(
        config.EXPECTED_TOTAL_COUNT,
        config.EXPECTED_TOTAL_COUNT
    )
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
    expected_finish_show_text = config.EXPECTED_SHOW_TEXT.format(
        expected_count,
        config.EXPECTED_TOTAL_COUNT
    )
    assert showing_text == expected_finish_show_text, \
        f"Expected {expected_finish_show_text}, got {showing_text}"
