import requests
from config.config import config


class ApiClient:
    """Клиент для работы с API MTS Shop"""

    def __init__(self, base_url=None):
        self.base_url = base_url or config.API_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def get_product_info(self, product_ids):
        """Получить информацию о товарах по ID"""
        if isinstance(product_ids, str):
            product_ids = [product_ids]

        params = {"id": product_ids} if len(product_ids) > 1 else {"id": product_ids[0]}
        return self._request("GET", "/products/prices", params=params)

    def add_to_cart(self, product_id, quantity=1, corporate=False):
        """Добавить товар в корзину"""
        payload = {
            "id": product_id,
            "quantity": quantity,
            "corporate": corporate
        }
        return self._request("POST", "/cart/add", json=payload)

    def get_cart(self, corporate=False):
        """Получить содержимое корзины"""
        params = {"corporate": str(corporate).lower()}
        return self._request("GET", "/cart", params=params)

    def clear_cart(self):
        """Очистить корзину"""
        return self._request("DELETE", "/cart")

    def _request(self, method, endpoint, **kwargs):
        """Базовый запрос"""
        url = f"{self.base_url}{endpoint}"
        if "timeout" not in kwargs:
            kwargs["timeout"] = 30

        return self.session.request(method, url, **kwargs)