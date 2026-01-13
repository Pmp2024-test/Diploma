import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from utils.api_client import ApiClient
from config.config import config


@pytest.fixture
def api_client():
    """Фикстура для API клиента"""
    return ApiClient()


@pytest.fixture
def auth_api_client():
    """Фикстура для авторизованного API клиента"""
    return ApiClient(api_token=config.API_TOKEN)


@pytest.fixture(scope="function")
def driver():
    """Фикстура для веб-драйвера"""
    browser = config.BROWSER
    driver = None

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        if config.HEADLESS:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        if config.HEADLESS:
            options.add_argument("--headless")

        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)

    else:
        raise ValueError(f"Unsupported browser: {browser}")

    # Настройки драйвера
    driver.implicitly_wait(config.IMPLICIT_WAIT)
    driver.set_page_load_timeout(30)

    yield driver

    # Закрываем браузер после теста
    if driver:
        driver.quit()


@pytest.fixture
def main_page(driver):
    """Фикстура для главной страницы"""
    from pages.main_page import MainPage
    page = MainPage(driver)
    page.open()
    return page


@pytest.fixture
def product_page(driver):
    """Фикстура для страницы товара"""
    from pages.product_page import ProductPage
    return ProductPage(driver)


@pytest.fixture
def cart_page(driver):
    """Фикстура для корзины"""
    from pages.cart_page import CartPage
    return CartPage(driver)


@pytest.fixture
def order_page(driver):
    """Фикстура для страницы оформления заказа"""
    from pages.order_page import OrderPage
    return OrderPage(driver)


@pytest.fixture(autouse=True)
def cleanup_cart(api_client):
    """Автоматически очищаем корзину после каждого теста"""
    yield
    try:
        api_client.clear_cart()
    except:
        pass  # Игнорируем ошибки при очистке


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для создания скриншотов при падении тестов"""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        try:
            # Делаем скриншот если тест упал
            driver = item.funcargs.get('driver')
            if driver:
                screenshot_path = config.SCREENSHOTS_DIR / f"{item.name}.png"
                driver.save_screenshot(str(screenshot_path))
                allure.attach.file(
                    str(screenshot_path),
                    name="screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
        except Exception as e:
            print(f"Не удалось сделать скриншот: {e}")
