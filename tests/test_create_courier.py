import pytest
import allure
from data import CourierData
from helpers import generate_courier_payload


class TestCreateCourier:
    """Набор тестов для ручки POST /api/v1/courier (Создание курьера)."""

    @allure.title("Успешное создание курьера со всеми валидными полями")
    @allure.description("Проверка: курьера можно создать, возвращается код 201 и {'ok': True}")
    def test_create_courier_success(self, courier_api, courier_cleanup):
        payload = generate_courier_payload()

        response = courier_api.create_courier(payload)

        # Логинимся для получения id и очистки курьера в teardown
        login_res = courier_api.login_courier({"login": payload["login"], "password": payload["password"]})
        if login_res.status_code == 200:
            courier_cleanup.append(login_res.json().get("id"))

        assert response.status_code == 201
        assert response.json() == {"ok": True}

    @allure.title("Нельзя создать двух одинаковых курьеров")
    @allure.description("Проверка: повторный запрос с теми же данными возвращает 409 и сообщение об ошибке")
    def test_cannot_create_two_identical_couriers(self, courier_api, courier_cleanup):
        payload = generate_courier_payload()

        # Создаем первого курьера
        first_response = courier_api.create_courier(payload)
        assert first_response.status_code == 201

        login_res = courier_api.login_courier({"login": payload["login"], "password": payload["password"]})
        if login_res.status_code == 200:
            courier_cleanup.append(login_res.json().get("id"))

        # Пытаемся создать второго идентичного курьера
        second_response = courier_api.create_courier(payload)

        assert second_response.status_code == 409
        assert second_response.json().get("message") == CourierData.ERROR_LOGIN_ALREADY_EXISTS

    @allure.title("Нельзя создать курьера с логином, который уже занят")
    @allure.description("Проверка: запрос с существующим логином и другим паролем возвращает 409")
    def test_create_courier_with_existing_login(self, courier_api, courier_cleanup):
        payload = generate_courier_payload()

        # Создаем первого курьера
        first_response = courier_api.create_courier(payload)
        assert first_response.status_code == 201

        login_res = courier_api.login_courier({"login": payload["login"], "password": payload["password"]})
        if login_res.status_code == 200:
            courier_cleanup.append(login_res.json().get("id"))

        # Создаем данные с тем же логином, но другим паролем
        another_payload = {
            "login": payload["login"],
            "password": "new_password_123",
            "firstName": "DifferentName"
        }
        second_response = courier_api.create_courier(another_payload)

        assert second_response.status_code == 409
        assert second_response.json().get("message") == CourierData.ERROR_LOGIN_ALREADY_EXISTS

    @allure.title("Ошибка при создании курьера без обязательного поля")
    @allure.description("Проверка: запрос без логина или без пароля возвращает 400 и текст ошибки")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_without_required_field(self, courier_api, missing_field):
        payload = generate_courier_payload()
        del payload[missing_field]

        response = courier_api.create_courier(payload)

        assert response.status_code == 400
        assert response.json().get("message") == CourierData.ERROR_CREDENTIALS_REQUIRED
