import allure
from api.order_api import OrderApi


class TestGetOrders:
    """Набор тестов для ручки GET /api/v1/orders (Список заказов)."""

    @allure.title("Получение списка заказов")
    @allure.description("Проверка: запрос возвращает статус 200, в теле ответа возвращается список заказов")
    def test_get_orders_returns_list_of_orders(self, order_api):
        response = order_api.get_orders_list(params={"limit": 10, "page": 0})

        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json().get("orders"), list)
        assert len(response.json().get("orders")) > 0
