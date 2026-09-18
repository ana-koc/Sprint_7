import pytest
from api.courier_api import CourierApi
from api.order_api import OrderApi
from helpers import generate_courier_payload


@pytest.fixture
def courier_api():
    """Экземпляр клиента для работы с курьерами."""
    return CourierApi()


@pytest.fixture
def order_api():
    """Экземпляр клиента для работы с заказами."""
    return OrderApi()


@pytest.fixture
def courier_cleanup(courier_api):
    """
    Фикстура-накопитель для автоматического удаления курьеров в teardown.
    Принимает в список:
      - id курьера (int / str)
      - или словарь с данными курьера ('login', 'password').
    После завершения теста все добавленные курьеры будут удалены.
    """
    couriers_to_delete = []
    yield couriers_to_delete
    for item in couriers_to_delete:
        if isinstance(item, dict):
            login_res = courier_api.login_courier({
                "login": item["login"],
                "password": item["password"]
            })
            if login_res.status_code == 200:
                cid = login_res.json().get("id")
                if cid:
                    courier_api.delete_courier(cid)
        elif item:
            courier_api.delete_courier(item)


@pytest.fixture
def created_courier(courier_api):
    """
    Фикстура для создания уникального курьера перед тестом
    и гарантированного удаления после выполнения теста.
    Возвращает словарь с данными курьера и его id:
    {'login': ..., 'password': ..., 'firstName': ..., 'id': ...}
    """
    payload = generate_courier_payload()
    # 1. Создаем курьера
    courier_api.create_courier(payload)

    # 2. Логинимся, чтобы получить id для последующего удаления
    login_response = courier_api.login_courier({
        "login": payload["login"],
        "password": payload["password"]
    })
    courier_id = login_response.json().get("id")

    payload["id"] = courier_id

    yield payload

    # 3. Teardown: удаляем курьера после теста
    if courier_id:
        courier_api.delete_courier(courier_id)
