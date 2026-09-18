import requests
import allure
from urls import Urls


class OrderApi:
    """Класс с методами для взаимодействия с API заказов."""

    @allure.step("Отправка запроса на создание заказа")
    def create_order(self, payload):
        return requests.post(Urls.ORDERS, json=payload)

    @allure.step("Отправка запроса на получение списка заказов")
    def get_orders_list(self, params=None):
        return requests.get(Urls.ORDERS, params=params)
