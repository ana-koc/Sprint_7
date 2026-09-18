import pytest
import allure
from data import CourierData
from helpers import generate_random_string


class TestLoginCourier:
    """Набор тестов для ручки POST /api/v1/courier/login (Логин курьера)."""

    @allure.title("Успешная авторизация курьера")
    @allure.description("Проверка: курьер может авторизоваться, возвращается статус 200 и id курьера")
    def test_login_courier_success(self, courier_api, created_courier):
        payload = {
            "login": created_courier["login"],
            "password": created_courier["password"]
        }

        response = courier_api.login_courier(payload)

        assert response.status_code == 200
        assert "id" in response.json()
        assert response.json()["id"] == created_courier["id"]

    @allure.title("Ошибка авторизации при отсутствии логина")
    @allure.description("Проверка: запрос без логина возвращает 400 и ошибку 'Недостаточно данных для входа'")
    def test_login_courier_without_login(self, courier_api, created_courier):
        payload = {
            "password": created_courier["password"]
        }

        response = courier_api.login_courier(payload)

        assert response.status_code == 400
        assert response.json().get("message") == CourierData.ERROR_LOGIN_CREDENTIALS_REQUIRED

    @allure.title("Ошибка авторизации при отсутствии пароля (баг бэкенда 504 Gateway Timeout)")
    @allure.description("Проверка: запрос без пароля должен возвращать 400. Помечен как xfail из-за бага сервера")
    @pytest.mark.xfail(reason="Баг сервиса: при отсутствии пароля запрос зависает и возвращает 504 вместо 400")
    def test_login_courier_without_password(self, courier_api, created_courier):
        payload = {
            "login": created_courier["login"]
        }

        response = courier_api.login_courier(payload)

        assert response.status_code == 400
        assert response.json().get("message") == CourierData.ERROR_LOGIN_CREDENTIALS_REQUIRED

    @allure.title("Ошибка авторизации с неправильным паролем")
    @allure.description("Проверка: запрос с неверным паролем возвращает 404 и текст ошибки")
    def test_login_courier_with_incorrect_password(self, courier_api, created_courier):
        payload = {
            "login": created_courier["login"],
            "password": f"{created_courier['password']}_wrong"
        }

        response = courier_api.login_courier(payload)

        assert response.status_code == 404
        assert response.json().get("message") == CourierData.ERROR_ACCOUNT_NOT_FOUND

    @allure.title("Ошибка авторизации с неправильным логином")
    @allure.description("Проверка: запрос с неверным логином возвращает 404 и текст ошибки")
    def test_login_courier_with_incorrect_login(self, courier_api, created_courier):
        payload = {
            "login": f"{created_courier['login']}_wrong",
            "password": created_courier["password"]
        }

        response = courier_api.login_courier(payload)

        assert response.status_code == 404
        assert response.json().get("message") == CourierData.ERROR_ACCOUNT_NOT_FOUND

    @allure.title("Ошибка авторизации под несуществующим пользователем")
    @allure.description("Проверка: авторизация случайного пользователя возвращает 404")
    def test_login_courier_non_existent_user(self, courier_api):
        payload = {
            "login": generate_random_string(12),
            "password": generate_random_string(12)
        }

        response = courier_api.login_courier(payload)

        assert response.status_code == 404
        assert response.json().get("message") == CourierData.ERROR_ACCOUNT_NOT_FOUND
