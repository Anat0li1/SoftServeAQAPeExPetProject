from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage
from pages.components.product_item import ProductItem
from pages.element import Element


class ProductsPage(BasePage):
    URL = "https://www.practiceqaautomation.com/shop"

    CART_LINK = Element(
        (By.CSS_SELECTOR, "a[data-testid='cart-link']")
    )

    ORDERS_LINK = Element(
        (By.CSS_SELECTOR, "a[data-testid='orders-link']")
    )

    NAV_PRODUCTS = Element(
        (By.CSS_SELECTOR, "a[data-testid='nav-products']")
    )

    SEARCH_INPUT = Element(
        (By.CSS_SELECTOR, "input[data-testid='search-input']")
    )

    SORT_SELECT = Element(
        (By.CSS_SELECTOR, "select[data-testid='sort-select']")
    )

    PRODUCT_CARDS = (
        By.CSS_SELECTOR,
        "li[data-testid='product-card']"
    )

    PRODUCT_NAMES = (
        By.CSS_SELECTOR,
        "a[data-testid='product-name']"
    )

    PRODUCT_PRICES = (
        By.CSS_SELECTOR,
        "span[data-testid='product-price']"
    )

    PRODUCT_COUNT = (
        By.XPATH,
        "//p[@data-testid='product-count']"
    )

    PRODUCT_ITEM = (
        By.XPATH,
        "//a[contains(text(), '{0}')]//ancestor::li"
    )

    def open_page(self):
        self.open(self.URL)

    def get_product(self, product_name):
        locator = (
            self.PRODUCT_ITEM[0],
            self.PRODUCT_ITEM[1].format(product_name)
        )

        element = self.wait.until(
            ec.visibility_of_element_located(locator)
        )

        return ProductItem(self.driver, element)

    def get_products_count(self):
        return len(self.find_elements(self.PRODUCT_CARDS))

    def get_product_names(self):
        elements = self.find_elements(self.PRODUCT_NAMES)
        return [element.text for element in elements]

    def get_product_prices(self):
        elements = self.find_elements(self.PRODUCT_PRICES)
        return [element.text for element in elements]

    def get_product_count_text(self):
        return self.get_text(self.PRODUCT_COUNT)

    def search_product(self, search_word):
        self.SEARCH_INPUT.clear()
        self.SEARCH_INPUT.send_keys(search_word)

    def sort_products(self, sort_value):
        Select(self.SORT_SELECT).select_by_value(sort_value)

    def open_cart(self):
        self.CART_LINK.click()

    def open_orders(self):
        self.ORDERS_LINK.click()

    def open_products(self):
        self.NAV_PRODUCTS.click()
