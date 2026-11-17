from selenium.webdriver.common.by import By

from pages.components.base_component import BaseComponent


class OrderSummary(BaseComponent):
    SUBTOTAL = (
        By.XPATH,
        ".//dt[normalize-space()='Subtotal']/following-sibling::dd"
    )

    SHIPPING = (
        By.XPATH,
        ".//dt[normalize-space()='Shipping']/following-sibling::dd"
    )

    DISCOUNT = (
        By.XPATH,
        ".//dt[contains(text(), 'Discount')]/following-sibling::dd"
    )

    TOTAL = (
        By.XPATH,
        ".//dt[normalize-space()='Total']/following-sibling::dd"
    )

    COUPON_INPUT = (
        By.CSS_SELECTOR,
        "input[data-testid='coupon-input']"
    )

    APPLY_COUPON_BUTTON = (
        By.CSS_SELECTOR,
        "button[data-testid='apply-coupon']"
    )

    COUPON_MESSAGE = (
        By.CSS_SELECTOR,
        "p[data-testid='coupon-message']"
    )

    CHECKOUT_BUTTON = (
        By.CSS_SELECTOR,
        "a[data-testid='checkout-button']"
    )

    def get_subtotal(self):
        return self.get_text(self.SUBTOTAL)

    def get_shipping(self):
        return self.get_text(self.SHIPPING)

    def get_discount(self):
        return self.get_text(self.DISCOUNT)

    def get_total(self):
        return self.get_text(self.TOTAL)

    def get_coupon_message(self):
        return self.get_text(self.COUPON_MESSAGE)

    def apply_coupon(self, promo_code):
        self.type_text(self.COUPON_INPUT, promo_code)
        self.click(self.APPLY_COUPON_BUTTON)

    def checkout(self):
        self.click(self.CHECKOUT_BUTTON)
