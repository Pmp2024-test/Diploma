from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from .base_page import BasePage
from .cart_page import CartPage


class ProductPage(BasePage):
    """Класс для работы со страницей товара"""

    # Локаторы
    PRODUCT_NAME = (By.CSS_SELECTOR, "[data-test='product-name'], .product-title")
    PRODUCT_PRICE = (By.CSS_SELECTOR, "[data-test='product-price'], .price")
    PRODUCT_DESCRIPTION = (By.CSS_SELECTOR, "[data-test='product-description'], .description")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "[data-test='add-to-cart'], .add-to-cart")
    QUANTITY_INPUT = (By.CSS_SELECTOR, "[data-test='quantity-input'], input[name='quantity']")
    QUANTITY_SELECT = (By.CSS_SELECTOR, "[data-test='quantity-select'], select[name='quantity']")
    BUY_NOW_BUTTON = (By.CSS_SELECTOR, "[data-test='buy-now'], .buy-now")
    BACK_BUTTON = (By.CSS_SELECTOR, "[data-test='back-button'], .back-button")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "[data-test='success-message'], .success-message")
    CHARACTERISTICS = (By.CSS_SELECTOR, "[data-test='characteristics'], .characteristics")
    IMAGES = (By.CSS_SELECTOR, "[data-test='product-image'], .product-image")

    def __init__(self, driver):
        super().__init__(driver)

    def get_product_name(self):
        """Получить название товара"""
        return self.get_text(self.PRODUCT_NAME)

    def get_product_price(self):
        """Получить цену товара"""
        price_text = self.get_text(self.PRODUCT_PRICE)
        # Очищаем цену от символов (оставляем только цифры)
        import re
        numbers = re.findall(r'\d+', price_text.replace(' ', ''))
        return float(''.join(numbers)) if numbers else 0

    def add_to_cart(self, quantity=1):
        """Добавить товар в корзину"""
        # Устанавливаем количество если есть поле
        if self.is_element_present(self.QUANTITY_INPUT):
            self.input_text(self.QUANTITY_INPUT, str(quantity))
        elif self.is_element_present(self.QUANTITY_SELECT):
            select = Select(self.find_element(self.QUANTITY_SELECT))
            select.select_by_value(str(quantity))

        # Добавляем в корзину
        self.click(self.ADD_TO_CART_BUTTON)

        # Проверяем сообщение об успехе
        if self.is_element_present(self.SUCCESS_MESSAGE, timeout=5):
            return self.get_text(self.SUCCESS_MESSAGE)
        return "Товар добавлен в корзину"

    def buy_now(self):
        """Купить сейчас (переход к оформлению)"""
        self.click(self.BUY_NOW_BUTTON)
        # Возвращаем CartPage или OrderPage в зависимости от реализации
        return CartPage(self.driver)

    def go_back(self):
        """Вернуться назад"""
        self.click(self.BACK_BUTTON)
        from .main_page import MainPage
        return MainPage(self.driver)

    def get_characteristics(self):
        """Получить характеристики товара"""
        if self.is_element_present(self.CHARACTERISTICS):
            chars_text = self.get_text(self.CHARACTERISTICS)
            # Парсим характеристики в словарь
            characteristics = {}
            lines = chars_text.split('\n')
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    characteristics[key.strip()] = value.strip()
            return characteristics
        return {}

    def is_available(self):
        """Проверить доступность товара"""
        try:
            # Ищем кнопку добавления в корзину
            add_button = self.find_element(self.ADD_TO_CART_BUTTON)
            return add_button.is_enabled() and "недоступен" not in add_button.text.lower()
        except:
            return False

    def get_images_count(self):
        """Получить количество изображений товара"""
        return len(self.find_elements(self.IMAGES))
