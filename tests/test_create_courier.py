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
        courier_cleanup.append(payload)

        response = courier_api.create_courier(payload)

        assert response.status_code == 201
        assert response.json() == {"ok": True}

    @allure.title("Нельзя создать двух одинаковых курьеров")
    @allure.description("Проверка: повторный запрос с теми же данными возвращает 409 и сообщение об ошибке")
    def test_cannot_create_two_identical_couriers(self, courier_api, created_courier):
        payload = {
            "login": created_courier["login"],
            "password": created_courier["password"],
            "firstName": created_courier["firstName"]
        }

        # Пытаемся создать второго идентичного курьера
        response = courier_api.create_courier(payload)

        assert response.status_code == 409
        assert response.json().get("message") == CourierData.ERROR_LOGIN_ALREADY_EXISTS

    @allure.title("Нельзя создать курьера с логином, который уже занят")
    @allure.description("Проверка: запрос с существующим логином и другим паролем возвращает 409")
    def test_create_courier_with_existing_login(self, courier_api, created_courier):
        # Создаем данные с тем же логином, но другим паролем
        another_payload = {
            "login": created_courier["login"],
            "password": "new_password_123",
            "firstName": "DifferentName"
        }
        response = courier_api.create_courier(another_payload)

        assert response.status_code == 409
        assert response.json().get("message") == CourierData.ERROR_LOGIN_ALREADY_EXISTS

    @allure.title("Ошибка при создании курьера без обязательного поля")
    @allure.description("Проверка: запрос без логина или без пароля возвращает 400 и текст ошибки")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_without_required_field(self, courier_api, missing_field):
        payload = generate_courier_payload()
        del payload[missing_field]

        response = courier_api.create_courier(payload)

        assert response.status_code == 400
        assert response.json().get("message") == CourierData.ERROR_CREDENTIALS_REQUIRED
