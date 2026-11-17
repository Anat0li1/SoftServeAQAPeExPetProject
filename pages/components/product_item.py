from selenium.webdriver.common.by import By

from pages.components.base_component import BaseComponent


class ProductItem(BaseComponent):
    PRODUCT_NAME = (
        By.CSS_SELECTOR,
        "a[data-testid='product-name']"
    )

    PRODUCT_BUTTON = (By.TAG_NAME, "button")

    PRODUCT_PRICE = (
        By.CSS_SELECTOR,
        "span[data-testid='product-price']"
    )

    def get_name(self):
        return self.get_text(self.PRODUCT_NAME)

    def get_price(self):
        return self.get_text(self.PRODUCT_PRICE)

    def get_button_text(self):
        return self.get_text(self.PRODUCT_BUTTON)

    def click_button(self):
        self.click(self.PRODUCT_BUTTON)