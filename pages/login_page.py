from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.products_page import ProductsPage


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.username_input_locator = (By.ID, "username")
        self.password_input_locator = (By.ID, "password")
        self.login_button_locator = (
            By.CSS_SELECTOR,
            "button[data-testid='login-button'], button[type='submit']"
        )

    def login(self, username, password):
        self.type_text(self.username_input_locator, username)
        self.type_text(self.password_input_locator, password)
        self.click(self.login_button_locator)
        return ProductsPage(self.driver)
