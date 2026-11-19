from selenium.webdriver.support import expected_conditions


class Element:
    def __init__(self, locator, clickable = False):
        self.locator = locator
        self.clickable = clickable

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self.clickable:
            return instance.wait_until_element_is_clickable(self.locator)
        return instance.wait.until(
            expected_conditions.visibility_of_element_located(self.locator)
        )
