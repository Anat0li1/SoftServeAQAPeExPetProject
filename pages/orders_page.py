from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class OrdersPage(BasePage):
    ORDERS_TABLE = (By.TAG_NAME, "table")

    ORDER_ROWS = (
        By.CSS_SELECTOR,
        "tr[data-testid='order-row']"
    )

    TABLE_HEADERS = (
        By.CSS_SELECTOR,
        "thead tr th"
    )

    def get_table(self):
        return self.wait_until_element_visible(self.TABLE_HEADERS)

    def get_order_rows(self):
        return self.find_elements(self.ORDER_ROWS)

    def get_headers(self):
        elements = self.find_elements(self.TABLE_HEADERS)
        return [element.text.lower() for element in elements]

    def get_cell_value(self, row, column_name):
        headers = self.get_headers()

        column_index = headers.index(column_name)

        cells = row.find_elements(By.TAG_NAME, "td")

        return cells[column_index].text

    def get_order_status(self, row):
        return row.find_element(By.CSS_SELECTOR, "td span").text
