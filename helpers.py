import random
import string
import requests
from urls import Urls


def generate_random_string(length=10):
    """Генерация случайной строки из букв нижнего регистра."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def generate_courier_payload():
    """Генерация уникального набора данных для создания курьера."""
    return {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10)
    }


def register_new_courier_and_return_login_password():
    """
    Метод регистрации нового курьера.
    Возвращает список из логина, пароля и имени курьера [login, password, firstName].
    Если регистрация не удалась, возвращает пустой список.
    """
    login_pass = []
    payload = generate_courier_payload()

    response = requests.post(Urls.COURIER, data=payload)

    if response.status_code == 201:
        login_pass.append(payload["login"])
        login_pass.append(payload["password"])
        login_pass.append(payload["firstName"])

    return login_pass
