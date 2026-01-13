from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from .base_page import BasePage
from .order_page import OrderPage


class CartPage(BasePage):
    """Класс для работы с корзиной"""

    # Локаторы
    CART_TITLE = (By.CSS_SELECTOR, "[data-test='cart-title'], h1")
    CART_ITEMS = (By.CSS_SELECTOR, "[data-test='cart-item'], .cart-item")
    ITEM_NAME = (By.CSS_SELECTOR, "[data-test='item-name'], .item-name")
    ITEM_PRICE = (By.CSS_SELECTOR, "[data-test='item-price'], .item-price")
    ITEM_QUANTITY = (By.CSS_SELECTOR, "[data-test='item-quantity'], .quantity")
    ITEM_TOTAL = (By.CSS_SELECTOR, "[data-test='item-total'], .item-total")
    REMOVE_BUTTON = (By.CSS_SELECTOR, "[data-test='remove-button'], .remove")
    CLEAR_CART_BUTTON = (By.CSS_SELECTOR, "[data-test='clear-cart'], .clear-cart")
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, "[data-test='checkout-button'], .checkout")
    CONTINUE_SHOPPING = (By.CSS_SELECTOR, "[data-test='continue-shopping'], .continue-shopping")
    CART_TOTAL = (By.CSS_SELECTOR, "[data-test='cart-total'], .total")
    EMPTY_CART_MESSAGE = (By.CSS_SELECTOR, "[data-test='empty-cart'], .empty-cart")
    QUANTITY_INPUT = (By.CSS_SELECTOR, "input[data-test='quantity-input']")
    QUANTITY_SELECT = (By.CSS_SELECTOR, "select[data-test='quantity-select']")

    def __init__(self, driver):
        super().__init__(driver)

    def is_empty(self):
        """Проверить пуста ли корзина"""
        return self.is_element_present(self.EMPTY_CART_MESSAGE) or \
            len(self.find_elements(self.CART_ITEMS)) == 0

    def get_items_count(self):
        """Получить количество товаров в корзине"""
        if self.is_empty():
            return 0
        return len(self.find_elements(self.CART_ITEMS))

    def get_total_price(self):
        """Получить общую сумму корзины"""
        if self.is_empty():
            return 0

        total_text = self.get_text(self.CART_TOTAL)
        import re
        numbers = re.findall(r'\d+', total_text.replace(' ', ''))
        return float(''.join(numbers)) if numbers else 0

    def get_item_details(self, index=0):
        """Получить детали товара по индексу"""
        if self.is_empty():
            return {}

        items = self.find_elements(self.CART_ITEMS)
        if index >= len(items):
            raise IndexError(f"Товар с индексом {index} не найден")

        item = items[index]
        return {
            'name': item.find_element(*self.ITEM_NAME).text.strip(),
            'price': self._extract_price(item.find_element(*self.ITEM_PRICE).text),
            'quantity': item.find_element(*self.ITEM_QUANTITY).text.strip(),
            'total': self._extract_price(item.find_element(*self.ITEM_TOTAL).text)
        }

    def _extract_price(self, price_text):
        """Извлечь цену из текста"""
        import re
        numbers = re.findall(r'\d+', price_text.replace(' ', ''))
        return float(''.join(numbers)) if numbers else 0

    def update_quantity(self, index=0, quantity=1):
        """Обновить количество товара"""
        if self.is_empty():
            raise ValueError("Корзина пуста")

        items = self.find_elements(self.CART_ITEMS)
        if index >= len(items):
            raise IndexError(f"Товар с индексом {index} не найден")

        item = items[index]

        # Пробуем найти поле ввода количества
        try:
            quantity_input = item.find_element(*self.QUANTITY_INPUT)
            quantity_input.clear()
            quantity_input.send_keys(str(quantity))
        except:
            try:
                quantity_select = item.find_element(*self.QUANTITY_SELECT)
                select = Select(quantity_select)
                select.select_by_value(str(quantity))
            except:
                raise ValueError("Не удалось изменить количество товара")

        # Ждем обновления
        self.wait_for_update()
        return self

    def wait_for_update(self, timeout=5):
        """Ожидание обновления корзины"""
        # Можно добавить ожидание спиннера или другого индикатора загрузки
        import time
        time.sleep(1)  # Простая задержка для примера

    def remove_item(self, index=0):
        """Удалить товар из корзины"""
        if self.is_empty():
            raise ValueError("Корзина пуста")

        items = self.find_elements(self.CART_ITEMS)
        if index >= len(items):
            raise IndexError(f"Товар с индексом {index} не найден")

        item = items[index]
        remove_btn = item.find_element(*self.REMOVE_BUTTON)
        remove_btn.click()

        # Подтверждение если нужно
        self._confirm_removal()
        return self

    def _confirm_removal(self):
        """Подтверждение удаления"""
        # Если есть диалог подтверждения
        try:
            confirm_btn = self.driver.find_element(
                By.CSS_SELECTOR, "[data-test='confirm-remove'], button:contains('Да')"
            )
            confirm_btn.click()
        except:
            pass  # Нет диалога подтверждения

    def clear_cart(self):
        """Очистить корзину полностью"""
        if not self.is_empty():
            self.click(self.CLEAR_CART_BUTTON)
            self._confirm_removal()
        return self

    def proceed_to_checkout(self):
        """Перейти к оформлению заказа"""
        self.click(self.CHECKOUT_BUTTON)
        return OrderPage(self.driver)

    def continue_shopping(self):
        """Продолжить покупки"""
        self.click(self.CONTINUE_SHOPPING)
        from .main_page import MainPage
        return MainPage(self.driver)
