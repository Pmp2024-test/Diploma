from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config.config import config


class BasePage:
    """Базовый класс для всех страниц"""

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
        self.base_url = config.BASE_URL

    def open(self, url=""):
        """Открыть страницу"""
        full_url = f"{self.base_url}{url}"
        self.driver.get(full_url)
        return self

    def find_element(self, locator, timeout=None):
        """Найти элемент с ожиданием"""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator, timeout=None):
        """Найти все элементы с ожиданием"""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator, timeout=None):
        """Кликнуть по элементу"""
        element = self.find_element(locator, timeout)
        element.click()
        return element

    def input_text(self, locator, text, timeout=None):
        """Ввести текст в поле"""
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)
        return element

    def get_text(self, locator, timeout=None):
        """Получить текст элемента"""
        element = self.find_element(locator, timeout)
        return element.text.strip()

    def is_element_present(self, locator, timeout=5):
        """Проверить наличие элемента"""
        try:
            self.find_element(locator, timeout)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def is_element_visible(self, locator, timeout=5):
        """Проверить видимость элемента"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.visibility_of_element_located(locator))
            return element.is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    def wait_for_url_contains(self, text, timeout=None):
        """Ожидание появления текста в URL"""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(EC.url_contains(text))

    def take_screenshot(self, name):
        """Сделать скриншот"""
        screenshot_path = config.SCREENSHOTS_DIR / f"{name}.png"
        self.driver.save_screenshot(str(screenshot_path))
        return screenshot_path
