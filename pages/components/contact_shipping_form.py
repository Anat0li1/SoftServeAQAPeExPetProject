from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.components.base_component import BaseComponent


class ContactShippingForm(BaseComponent):
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    EMAIL = (By.ID, "email")
    PHONE = (By.ID, "phone")
    ADDRESS = (By.ID, "address")
    CITY = (By.ID, "city")
    STATE = (By.ID, "state")
    ZIP_CODE = (By.ID, "zip")

    def fill(self, data):
        self.type_text(self.FIRST_NAME, data["first_name"])
        self.type_text(self.LAST_NAME, data["last_name"])
        self.type_text(self.EMAIL, data["email"])
        self.type_text(self.PHONE, data["phone"])
        self.type_text(self.ADDRESS, data["address"])
        self.type_text(self.CITY, data["city"])

        Select(self.find(self.STATE)).select_by_value(data["state"])

        self.type_text(self.ZIP_CODE, data["zip"])