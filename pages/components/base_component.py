class BaseComponent:
    def __init__(self, driver, root):
        self.driver = driver
        self.root = root

    def find(self, locator):
        return self.root.find_element(*locator)

    def find_all(self, locator):
        return self.root.find_elements(*locator)

    def click(self, locator):
        self.find(locator).click()

    def type_text(self, locator, value):
        element = self.find(locator)
        element.clear()
        element.send_keys(value)

    def get_text(self, locator):
        return self.find(locator).text