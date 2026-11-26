from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.products_page import ProductsPage


class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, "username")

    PASSWORD_INPUT = (By.ID, "password")

    LOGIN_BUTTON = (
        By.CSS_SELECTOR,
        "button[data-testid='login-button'], button[type='submit']"
    )

    ERROR_MESSAGE = (By.CSS_SELECTOR, "p[data-testid='login-error']")

    def login(self, username, password):
        self.submit_login(username, password)
        return ProductsPage(self.driver)

    def submit_login(self, username, password):
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
