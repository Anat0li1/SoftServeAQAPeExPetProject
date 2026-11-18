from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self, driver, wait = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, wait)

    def get_title(self):
        return self.driver.title

    def get_current_url(self):
        return self.driver.current_url

    def wait_until_element_visible(self, locator):
        return self.wait.until(ec.visibility_of_element_located(locator))

    def wait_until_element_invisible(self, locator):
        return self.wait.until(ec.invisibility_of_element_located(locator))

    def wait_until_element_clickable(self, locator):
        return self.wait.until(ec.element_to_be_clickable(locator))

    def is_visible(self, locator):
        try:
            self.wait_until_element_visible(locator)
            return True
        except TimeoutException:
            return False

    def is_invisible(self, locator):
        try:
            self.wait_until_element_invisible(locator)
            return True
        except TimeoutException:
            return False

    def click(self, locator):
        self.wait_until_element_clickable(locator).click()

    def type_text(self, locator, text):
        element = self.wait_until_element_visible(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.wait_until_element_visible(locator).text

    def open(self, url):
        self.driver.get(url)

    def find_element(self, locator):
        return self.wait.until(ec.presence_of_element_located(locator))

    def find_elements(self, locator):
        return self.wait.until(ec.presence_of_all_elements_located(locator))
