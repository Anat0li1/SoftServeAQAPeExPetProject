
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to use: chrome or firefox",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run in headless mode",
    )


@pytest.fixture(scope="function")
def driver(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    if browser == "firefox":
        firefox_options = FirefoxOptions()
        if headless:
            firefox_options.add_argument("--headless")
        browser_driver = webdriver.Firefox(options=firefox_options)
    elif browser == "chrome":
        chrome_options = ChromeOptions()
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        }
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument(
            "--disable-features=PasswordLeakDetection,"
            "PasswordManagerLeakDetection,AutofillServerCommunication"
        )
        chrome_options.add_argument("--disable-save-password-bubble")
        if headless:
            chrome_options.add_argument("--headless")
        browser_driver = webdriver.Chrome(options=chrome_options)
    else:
        raise Exception(f"Unsupported browser: {browser}")

    browser_driver.maximize_window()
    yield browser_driver
    browser_driver.quit()
