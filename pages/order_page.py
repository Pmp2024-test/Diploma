from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from .base_page import BasePage


class OrderPage(BasePage):
    """Класс для работы со страницей оформления заказа"""

    # Локаторы формы
    NAME_INPUT = (By.CSS_SELECTOR, "[data-test='name-input'], input[name='name']")
    PHONE_INPUT = (By.CSS_SELECTOR, "[data-test='phone-input'], input[name='phone']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "[data-test='email-input'], input[name='email']")
    ADDRESS_INPUT = (By.CSS_SELECTOR, "[data-test='address-input'], textarea[name='address']")
    CITY_SELECT = (By.CSS_SELECTOR, "[data-test='city-select'], select[name='city']")
    DELIVERY_METHOD = (By.CSS_SELECTOR, "[data-test='delivery-method'], input[name='delivery']")
    PAYMENT_METHOD = (By.CSS_SELECTOR, "[data-test='payment-method'], input[name='payment']")
    COMMENT_INPUT = (By.CSS_SELECTOR, "[data-test='comment-input'], textarea[name='comment']")

    # Кнопки
    SUBMIT_ORDER_BUTTON = (By.CSS_SELECTOR, "[data-test='submit-order'], button[type='submit']")
    BACK_TO_CART_BUTTON = (By.CSS_SELECTOR, "[data-test='back-to-cart'], .back-to-cart")

    # Информация о заказе
    ORDER_SUMMARY = (By.CSS_SELECTOR, "[data-test='order-summary'], .order-summary")
    ORDER_ITEMS = (By.CSS_SELECTOR, "[data-test='order-items'], .order-items")
    ORDER_TOTAL = (By.CSS_SELECTOR, "[data-test='order-total'], .order-total")

    # Сообщения
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "[data-test='success-message'], .success-message")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error-message'], .error-message")
    VALIDATION_ERROR = (By.CSS_SELECTOR, "[data-test='validation-error'], .error")

    def __init__(self, driver):
        super().__init__(driver)

    def fill_personal_info(self, name, phone, email):
        """Заполнить персональную информацию"""
        self.input_text(self.NAME_INPUT, name)
        self.input_text(self.PHONE_INPUT, phone)
        self.input_text(self.EMAIL_INPUT, email)
        return self

    def fill_address(self, address, city=None):
        """Заполнить адрес"""
        self.input_text(self.ADDRESS_INPUT, address)
        if city and self.is_element_present(self.CITY_SELECT):
            select = Select(self.find_element(self.CITY_SELECT))
            select.select_by_visible_text(city)
        return self

    def select_delivery_method(self, method="courier"):
        """Выбрать способ доставки"""
        delivery_methods = self.find_elements(self.DELIVERY_METHOD)
        for dm in delivery_methods:
            if method in dm.get_attribute("value") or method in dm.get_attribute("id"):
                dm.click()
                break
        return self

    def select_payment_method(self, method="card"):
        """Выбрать способ оплаты"""
        payment_methods = self.find_elements(self.PAYMENT_METHOD)
        for pm in payment_methods:
            if method in pm.get_attribute("value") or method in pm.get_attribute("id"):
                pm.click()
                break
        return self

    def add_comment(self, comment):
        """Добавить комментарий к заказу"""
        self.input_text(self.COMMENT_INPUT, comment)
        return self

    def submit_order(self):
        """Отправить заказ"""
        self.click(self.SUBMIT_ORDER_BUTTON)
        return self

    def get_order_summary(self):
        """Получить сводку заказа"""
        if self.is_element_present(self.ORDER_SUMMARY):
            return self.get_text(self.ORDER_SUMMARY)
        return ""

    def get_order_total(self):
        """Получить итоговую сумму заказа"""
        if self.is_element_present(self.ORDER_TOTAL):
            total_text = self.get_text(self.ORDER_TOTAL)
            import re
            numbers = re.findall(r'\d+', total_text.replace(' ', ''))
            return float(''.join(numbers)) if numbers else 0
        return 0

    def is_order_successful(self):
        """Проверить успешность оформления заказа"""
        return self.is_element_present(self.SUCCESS_MESSAGE, timeout=10)

    def get_success_message(self):
        """Получить сообщение об успешном оформлении"""
        if self.is_order_successful():
            return self.get_text(self.SUCCESS_MESSAGE)
        return ""

    def has_errors(self):
        """Проверить наличие ошибок"""
        return self.is_element_present(self.ERROR_MESSAGE) or \
            len(self.find_elements(self.VALIDATION_ERROR)) > 0

    def get_errors(self):
        """Получить список ошибок"""
        errors = []

        if self.is_element_present(self.ERROR_MESSAGE):
            errors.append(self.get_text(self.ERROR_MESSAGE))

        validation_errors = self.find_elements(self.VALIDATION_ERROR)
        for error in validation_errors:
            errors.append(error.text.strip())

        return errors

    def back_to_cart(self):
        """Вернуться в корзину"""
        self.click(self.BACK_TO_CART_BUTTON)
        from .cart_page import CartPage
        return CartPage(self.driver)

    def fill_all_required_fields(self, order_data):
        """Заполнить все обязательные поля"""
        # Персональные данные
        if 'name' in order_data:
            self.input_text(self.NAME_INPUT, order_data['name'])
        if 'phone' in order_data:
            self.input_text(self.PHONE_INPUT, order_data['phone'])
        if 'email' in order_data:
            self.input_text(self.EMAIL_INPUT, order_data['email'])

        # Адрес
        if 'address' in order_data:
            self.input_text(self.ADDRESS_INPUT, order_data['address'])
        if 'city' in order_data and self.is_element_present(self.CITY_SELECT):
            select = Select(self.find_element(self.CITY_SELECT))
            select.select_by_visible_text(order_data['city'])

        # Доставка и оплата
        if 'delivery' in order_data:
            self.select_delivery_method(order_data['delivery'])
        if 'payment' in order_data:
            self.select_payment_method(order_data['payment'])

        # Комментарий
        if 'comment' in order_data:
            self.add_comment(order_data['comment'])

        return self
