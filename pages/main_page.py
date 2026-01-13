from selenium.webdriver.common.by import By
from .base_page import BasePage
from .product_page import ProductPage
from .cart_page import CartPage


class MainPage(BasePage):
    """Класс для работы с главной страницей"""

    # Локаторы
    LOGO = (By.CSS_SELECTOR, "[data-test='logo'], .logo")
    SEARCH_INPUT = (By.CSS_SELECTOR, "[data-test='search-input'], input[type='search']")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "[data-test='search-button'], button[type='submit']")
    CART_BUTTON = (By.CSS_SELECTOR, "[data-test='cart-button'], .cart-icon")
    CATALOG_BUTTON = (By.CSS_SELECTOR, "[data-test='catalog-button'], .catalog")
    USER_PROFILE = (By.CSS_SELECTOR, "[data-test='user-profile'], .profile")
    PRODUCT_CARDS = (By.CSS_SELECTOR, "[data-test='product-card'], .product-card")
    CATEGORIES = (By.CSS_SELECTOR, "[data-test='category'], .category")

    def __init__(self, driver):
        super().__init__(driver)

    def is_loaded(self):
        """Проверка загрузки страницы"""
        return (
                self.is_element_present(self.LOGO) and
                self.is_element_present(self.SEARCH_INPUT) and
                self.is_element_present(self.CART_BUTTON)
        )

    def search_product(self, product_name):
        """Поиск товара"""
        self.input_text(self.SEARCH_INPUT, product_name)
        self.click(self.SEARCH_BUTTON)
        # Возвращаем эту же страницу для проверки результатов
        return self

    def get_search_results_count(self):
        """Получить количество результатов поиска"""
        return len(self.find_elements(self.PRODUCT_CARDS))

    def open_product_by_index(self, index=0):
        """Открыть товар по индексу"""
        products = self.find_elements(self.PRODUCT_CARDS)
        if index < len(products):
            products[index].click()
            return ProductPage(self.driver)
        raise IndexError(f"Товар с индексом {index} не найден")

    def open_product_by_name(self, product_name):
        """Открыть товар по названию"""
        products = self.find_elements(self.PRODUCT_CARDS)
        for product in products:
            try:
                # Пытаемся найти название товара в карточке
                name_element = product.find_element(
                    By.CSS_SELECTOR, "[data-test='product-name'], .product-name"
                )
                if product_name.lower() in name_element.text.lower():
                    product.click()
                    return ProductPage(self.driver)
            except:
                continue
        raise ValueError(f"Товар '{product_name}' не найден")

    def open_cart(self):
        """Открыть корзину"""
        self.click(self.CART_BUTTON)
        return CartPage(self.driver)

    def open_catalog(self):
        """Открыть каталог"""
        self.click(self.CATALOG_BUTTON)
        return self

    def select_category(self, category_name):
        """Выбрать категорию"""
        categories = self.find_elements(self.CATEGORIES)
        for category in categories:
            if category_name.lower() in category.text.lower():
                category.click()
                return self
        raise ValueError(f"Категория '{category_name}' не найдена")

    def get_cart_items_count(self):
        """Получить количество товаров в корзине (из счетчика)"""
        try:
            cart_counter = self.driver.find_element(
                By.CSS_SELECTOR, "[data-test='cart-counter'], .cart-counter"
            )
            return int(cart_counter.text)
        except:
            return 0
