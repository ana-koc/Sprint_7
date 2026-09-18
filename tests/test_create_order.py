import pytest
import allure
from data import OrderData


class TestCreateOrder:
    """Набор тестов для ручки POST /api/v1/orders (Создание заказа)."""

    @allure.title("Создание заказа с различными вариациями цветов")
    @allure.description("Проверка: заказ успешно создается с цветом BLACK, GREY, обоими цветами или без указания цвета. Тело ответа содержит track")
    @pytest.mark.parametrize("color", OrderData.COLOR_OPTIONS)
    def test_create_order_with_different_colors(self, order_api, color):
        payload = OrderData.DEFAULT_ORDER_BODY.copy()
        payload["color"] = color

        response = order_api.create_order(payload)

        assert response.status_code == 201
        assert "track" in response.json()
        assert isinstance(response.json().get("track"), int)
