from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from pages.base_page import BasePage
from pages.components.order_success import OrderSuccess


class ConfirmationPage(BasePage):
    SUCCESS_PANEL = (
        By.CSS_SELECTOR,
        "div[data-testid='order-success']"
    )

    def get_success_panel(self):
        element = self.wait.until(
            ec.visibility_of_element_located(self.SUCCESS_PANEL)
        )

        return OrderSuccess(self.driver, element)
