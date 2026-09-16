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
    В тесте можно передать courier_id в список: courier_cleanup.append(courier_id).
    После завершения теста все добавленные курьеры будут удалены.
    """
    courier_ids = []
    yield courier_ids
    for cid in courier_ids:
        if cid:
            courier_api.delete_courier(cid)


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
    create_response = courier_api.create_courier(payload)
    assert create_response.status_code == 201, "Не удалось создать тестового курьера"

    # 2. Логинимся, чтобы получить id для последующего удаления
    login_response = courier_api.login_courier({
        "login": payload["login"],
        "password": payload["password"]
    })
    assert login_response.status_code == 200, "Не удалось залогиниться для получения id курьера"
    courier_id = login_response.json().get("id")

    payload["id"] = courier_id

    yield payload

    # 3. Teardown: удаляем курьера после теста
    if courier_id:
        courier_api.delete_courier(courier_id)
