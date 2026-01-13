import pytest
import allure
from config.config import config


@allure.epic("MTS Shop API")
@allure.feature("API Тесты")
@pytest.mark.api
class TestMTSShopAPI:

    @allure.title("API-POS-001: Информация о товарах")
    @pytest.mark.positive
    def test_get_product_info(self, api_client):
        """Тест получения информации о товарах"""
        product_ids = ["708888", "708882", "708870", "947478"]

        with allure.step(f"Запрос информации о товарах {product_ids}"):
            response = api_client.get_product_info(product_ids)

        with allure.step("Проверка статус кода 200"):
            assert response.status_code == 200, \
                f"Ожидался статус 200, получен {response.status_code}"

        with allure.step("Проверка структуры ответа"):
            data = response.json()
            assert isinstance(data, list), "Ответ должен быть списком"
            assert len(data) > 0, "Список товаров не должен быть пустым"

            # Проверяем структуру первого товара
            product = data[0]
            assert "id" in product, "Товар должен иметь поле 'id'"
            assert "price" in product, "Товар должен иметь поле 'price'"

    @allure.title("API-POS-002: Добавить товар в корзину")
    @pytest.mark.positive
    def test_add_to_cart(self, api_client):
        """Тест добавления товара в корзину"""
        product_id = config.TEST_PRODUCT_ID

        with allure.step(f"Добавление товара {product_id} в корзину"):
            response = api_client.add_to_cart(product_id=product_id, quantity=1) # noqa: E501

        with allure.step("Проверка успешного добавления"):
            assert response.status_code in [200, 201], \
                f"Ожидался статус 200/201, получен {response.status_code}"

            # Сохраняем item_id для следующих тестов если нужно
            response_data = response.json()
            if "item_id" in response_data:
                self.item_id = response_data["item_id"]

    @allure.title("API-POS-003: Получить корзину")
    @pytest.mark.positive
    def test_get_cart(self, api_client):
        """Тест получения содержимого корзины"""
        with allure.step("Добавляем товар для теста"):
            api_client.add_to_cart(product_id=config.TEST_PRODUCT_ID)

        with allure.step("Получение содержимого корзины"):
            response = api_client.get_cart(corporate=False)

        with allure.step("Проверка статус кода 200"):
            assert response.status_code == 200, \
                f"Ожидался статус 200, получен {response.status_code}"

        with allure.step("Проверка структуры ответа"):
            cart_data = response.json()
            # Структура может быть разной, проверяем базовые поля
            assert "items" in cart_data or "products" in cart_data, \
                "Корзина должна содержать список товаров"

    @allure.title("API-NEG-001: Пустой ID товара при добавлении")
    @pytest.mark.negative
    def test_add_empty_product_id(self, api_client):
        """Тест добавления товара с пустым ID"""
        response = api_client.add_to_cart(product_id="")
        assert response.status_code == 400, \
            f"Ожидался статус 400 для пустого ID, получен {response.status_code}" # noqa: E501

    @allure.title("API-NEG-002: Добавление несуществующего товара")
    @pytest.mark.negative
    def test_add_nonexistent_product(self, api_client):
        """Тест добавления несуществующего товара"""
        response = api_client.add_to_cart(product_id="999999999")
        assert response.status_code in [404, 400], \
            f"Ожидался 404/400 для несуществующего товара, получен {response.status_code}" # noqa: E501
