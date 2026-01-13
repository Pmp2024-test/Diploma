import requests
import json


def check_api_endpoint():
    """Проверка API endpoint для диагностики"""

    # Пробуем разные возможные URL (подставьте ваши)
    endpoints = [
        'https://api.shop.mts.ru/api/products',
        'http://localhost:8000/api/products',
        'http://127.0.0.1:8000/api/products',
        '/api/products'  # относительный путь
    ]

    for url in endpoints:
        print(f"\n{'=' * 60}")
        print(f"Проверяем: {url}")
        print('=' * 60)

        try:
            # Добавляем базовый URL если нужно
            if not url.startswith('http'):
                url = 'http://localhost:8000' + url

            response = requests.get(url, timeout=10)

            print(f"Status Code: {response.status_code}")
            print(f"Content-Type: {response.headers.get('Content-Type')}")
            print(f"Response size: {len(response.text)} chars")

            if response.text:
                # Пробуем распарсить как JSON
                try:
                    data = response.json()
                    print("✓ Ответ - валидный JSON")
                    print(
                        f"JSON keys: {list(data.keys()) if isinstance(data, dict) else 'List length: ' + str(len(data))}")
                except json.JSONDecodeError:
                    print("✗ Ответ не JSON")
                    # Показываем начало ответа
                    preview = response.text[:300].replace('\n', ' ')
                    print(f"Preview: {preview}...")
            else:
                print("Пустой ответ")

        except requests.exceptions.RequestException as e:
            print(f"Ошибка подключения: {e}")
        except Exception as e:
            print(f"Другая ошибка: {e}")


if __name__ == "__main__":
    check_api_endpoint()
