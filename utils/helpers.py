import random
import string
from datetime import datetime
from typing import Dict, Any
from utils import generate_random_email, wait_for_element


def generate_random_string(length=10):
    """Сгенерировать случайную строку"""
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))


def generate_random_email():
    """Сгенерировать случайный email"""
    username = generate_random_string(8).lower()
    domain = random.choice(["gmail.com", "yahoo.com", "mail.ru", "yandex.ru"])
    return f"{username}@{domain}"


def generate_random_phone():
    """Сгенерировать случайный номер телефона"""
    prefix = random.choice(["+7", "+375", "+380"])
    number = ''.join([str(random.randint(0, 9)) for _ in range(10)])
    return f"{prefix}{number}"


def get_current_timestamp():
    """Получить текущую метку времени"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def validate_response_schema(response_data: Dict[str, Any], expected_schema: Dict[str, type]):
    """
    Валидация схемы ответа

    Пример:
    schema = {
        "id": str,
        "name": str,
        "price": (int, float),
        "available": bool
    }
    """
    errors = []

    for field, expected_type in expected_schema.items():
        if field not in response_data:
            errors.append(f"Отсутствует обязательное поле: {field}")
        else:
            value = response_data[field]
            if not isinstance(expected_type, tuple):
                expected_type = (expected_type,)

            if not any(isinstance(value, t) for t in expected_type):
                errors.append(
                    f"Поле {field} имеет тип {type(value).__name__}, "
                    f"ожидался {[t.__name__ for t in expected_type]}"
                )

    if errors:
        raise AssertionError(f"Ошибки валидации схемы:\n" + "\n".join(errors))

    return True


def wait_for_condition(condition_func, timeout=10, interval=0.5, message=""):
    """
    Ожидание выполнения условия

    Args:
        condition_func: функция, возвращающая bool
        timeout: максимальное время ожидания
        interval: интервал проверки
        message: сообщение при таймауте
    """
    import time
    start_time = time.time()

    while time.time() - start_time < timeout:
        if condition_func():
            return True
        time.sleep(interval)

    raise TimeoutError(message or f"Условие не выполнено за {timeout} секунд")
