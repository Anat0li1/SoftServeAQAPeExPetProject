from pages.login_page import LoginPage


def test_login_with_valid_credentials(driver, config):
    driver.get(config.BASE_URL)

    login_page = LoginPage(driver)

    expected_url = login_page.get_current_url()

    login_page.submit_login(config.LOCKED_USERNAME,
                            config.TEST_PASSWORD)

    actual_error = login_page.get_text(login_page.ERROR_MESSAGE)
    assert actual_error == config.LOCKED_ERROR_MESSAGE, \
        f"Expected: {config.LOCKED_ERROR_MESSAGE}, got {actual_error}"
    actual_url = login_page.get_current_url()
    assert actual_url == expected_url, \
        f"Expected: {expected_url}, got {actual_url}"
