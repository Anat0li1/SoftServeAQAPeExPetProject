from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from pages.base_page import BasePage
from pages.components.contact_shipping_form import ContactShippingForm
from pages.components.payment_form import PaymentForm
from pages.confirmation_page import ConfirmationPage


class CheckoutPage(BasePage):
    CONTACT_FORM = (
        By.XPATH,
        "//h2[contains(text(), 'Contact')]/ancestor::section"
    )

    PAYMENT_FORM = (
        By.XPATH,
        "//h2[contains(text(), 'Payment')]/ancestor::section"
    )

    ACCEPT_TERMS = (
        By.CSS_SELECTOR,
        "input[data-testid='accept-terms'], input[type='checkbox']"
    )

    PLACE_ORDER_BUTTON = (
        By.CSS_SELECTOR,
        "button[data-testid='place-order'], button[type='submit']"
    )

    ERROR_ELEMENTS = (
        By.XPATH,
        "//div[@role='alert']"
    )

    def get_contact_form(self):
        element = self.wait.until(
            ec.visibility_of_element_located(self.CONTACT_FORM)
        )

        return ContactShippingForm(self.driver, element)

    def get_payment_form(self):
        element = self.wait.until(
            ec.visibility_of_element_located(self.PAYMENT_FORM)
        )

        return PaymentForm(self.driver, element)

    def place_order(self):
        self.click(self.ACCEPT_TERMS)
        self.click(self.PLACE_ORDER_BUTTON)
        return ConfirmationPage(self.driver)

    def get_errors(self):
        return self.driver.find_elements(*self.ERROR_ELEMENTS)
