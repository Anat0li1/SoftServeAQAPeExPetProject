from pages.login_page import LoginPage


def test_login_with_valid_credentials(driver, config):
    driver.get(config.BASE_URL)

    login_page = LoginPage(driver)
    assert config.EXPECTED_TITLE in login_page.get_title(), \
        f"Expected {config.EXPECTED_TITLE} in the page title"

    products_page = login_page.login(config.TEST_USERNAME,
                                     config.TEST_PASSWORD)
    actual_greeting = products_page.get_greetings_text()
    expected_greeting = config.EXPECTED_GREETING.format(config.TEST_USERNAME)
    assert actual_greeting == expected_greeting, \
        f"Expected '{expected_greeting}', got '{actual_greeting}'"
    total_items = products_page.get_products_count()
    assert total_items == config.EXPECTED_TOTAL_COUNT, \
        f"Expected {config.EXPECTED_COUNT} items, got {total_items}"
    actual_showing_text = products_page.get_product_count_text()
    expected_showing_text = config.EXPECTED_SHOW_TEXT.format(
        config.EXPECTED_TOTAL_COUNT,
        config.EXPECTED_TOTAL_COUNT
    )
    assert actual_showing_text == expected_showing_text, \
        f"Expected '{expected_showing_text}', got '{actual_showing_text}'"
