from selenium.webdriver.common.by import By

from pages.components.base_component import BaseComponent


class PaymentForm(BaseComponent):
    CARD_NAME = (By.ID, "card-name")
    CARD_NUMBER = (By.ID, "card-number")
    CARD_EXPIRY = (By.ID, "card-expiry")
    CARD_CVV = (By.ID, "card-cvv")

    def fill(self, data):
        self.type_text(self.CARD_NAME, data["card_name"])
        self.type_text(self.CARD_NUMBER, data["card_number"])
        self.type_text(self.CARD_EXPIRY, data["expiry"])
        self.type_text(self.CARD_CVV, data["cvv"])