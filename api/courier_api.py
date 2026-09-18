import requests
import allure
from urls import Urls


class CourierApi:
    """Класс с методами для взаимодействия с API курьера."""

    @allure.step("Отправка запроса на создание курьера")
    def create_courier(self, payload):
        return requests.post(Urls.COURIER, data=payload)

    @allure.step("Отправка запроса на логин курьера")
    def login_courier(self, payload):
        return requests.post(Urls.COURIER_LOGIN, data=payload)

    @allure.step("Отправка запроса на удаление курьера")
    def delete_courier(self, courier_id):
        # Передаем id и в path, и в теле запроса для полной совместимости
        return requests.delete(f"{Urls.COURIER}/{courier_id}", data={"id": courier_id})
