from selenium.webdriver.common.by import By

from pages.components.base_component import BaseComponent


class OrderSuccess(BaseComponent):
    TITLE = (By.TAG_NAME, "h1")

    ORDER_ID = (
        By.CSS_SELECTOR,
        "p[data-testid='order-id']"
    )

    ORDER_ITEMS = (
        By.CSS_SELECTOR,
        "dd[data-testid='order-items']"
    )

    ORDER_TOTAL = (
        By.CSS_SELECTOR,
        "dd[data-testid='order-total']"
    )

    VIEW_ORDERS_BUTTON = (
        By.CSS_SELECTOR,
        "a[data-testid='view-orders']"
    )

    def get_delivery(self, label):
        locator = (
            By.XPATH,
            f".//dt[normalize-space()='{label}']/following-sibling::dd"
        )
        return self.get_text(locator)

    def get_payment(self, label):
        locator = (
            By.XPATH,
            f".//dt[normalize-space()='{label}']/following-sibling::dd"
        )
        return self.get_text(locator)

    def get_title(self):
        return self.get_text(self.TITLE)

    def get_order_id(self):
        return self.get_text(self.ORDER_ID)

    def get_items_count(self):
        return int(self.get_text(self.ORDER_ITEMS))

    def get_total(self):
        return self.get_text(self.ORDER_TOTAL)

    def open_orders(self):
        self.click(self.VIEW_ORDERS_BUTTON)