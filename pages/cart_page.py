from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from pages.base_page import BasePage
from pages.checkout_page import CheckoutPage
from pages.components.order_summary import OrderSummary


class CartPage(BasePage):
    CART_ITEMS = (
        By.CSS_SELECTOR,
        "li[data-testid='cart-item']"
    )

    CART_ITEM_PRICES = (
        By.XPATH,
        "//div[contains(text(), '$')]"
    )

    ORDER_SUMMARY = (By.TAG_NAME, "aside")

    CHECKOUT_BUTTON = (By.XPATH, "//a[@data-testid='checkout-button']")

    def get_cart_items(self):
        return self.find_elements(self.CART_ITEMS)

    def get_cart_item_prices(self):
        elements = self.find_elements(self.CART_ITEM_PRICES)
        return [element.text for element in elements]

    def get_order_summary(self):
        element = self.wait.until(
            ec.visibility_of_element_located(self.ORDER_SUMMARY)
        )

        return OrderSummary(self.driver, element)

    def open_checkout(self):
        self.click(self.CHECKOUT_BUTTON)
        return CheckoutPage(self.driver)

