"""
Конфигурация проекта MTS Shop Autotests
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Базовые пути
BASE_DIR = Path(__file__).parent.parent


class Config:
    """Основные настройки"""

    # URL
    BASE_URL = os.getenv("BASE_URL", "https://shop.mts.ru")
    API_BASE_URL = os.getenv("API_BASE_URL", "https://shop.mts.ru/api/v1")

    # Данные тестового товара
    TEST_PRODUCT_ID = os.getenv("TEST_PRODUCT_ID", "708888")
    TEST_PRODUCT_NAME = os.getenv("TEST_PRODUCT_NAME", "Смартфон")

    # Учетные данные
    TEST_USERNAME = os.getenv("TEST_USERNAME", "")
    TEST_PASSWORD = os.getenv("TEST_PASSWORD", "")
    API_TOKEN = os.getenv("API_TOKEN", "")

     # Настройки браузера
    BROWSER = os.getenv("BROWSER", "chrome").lower()
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "10"))
    WINDOW_WIDTH = int(os.getenv("WINDOW_WIDTH", "1920"))  # Добавь эту строку
    WINDOW_HEIGHT = int(os.getenv("WINDOW_HEIGHT", "1080"))  # И эту

    # Настройки API
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))
    API_MAX_RETRIES = int(os.getenv("API_MAX_RETRIES", "3"))

    # Пути
    SCREENSHOTS_DIR = BASE_DIR / "screenshots"
    REPORTS_DIR = BASE_DIR / "reports"
    LOGS_DIR = BASE_DIR / "logs"

    # Создаем директории
    for directory in [SCREENSHOTS_DIR, REPORTS_DIR, LOGS_DIR]:
        directory.mkdir(exist_ok=True)

    # Настройки тестов
    TEST_MODE = os.getenv("TEST_MODE", "all")  # all, ui, api


# Создаем экземпляр конфигурации
config = Config()
