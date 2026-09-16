# Финальный проект 7 спринта: Автоматизация тестирования API Яндекс Самокат

Проект содержит автоматизированные тесты для учебного сервиса **Яндекс Самокат** (https://qa-scooter.education-services.ru/).

## Стек технологий
- Python 3
- pytest
- requests
- allure-pytest

## Структура проекта
- `api/` — API-клиенты (`CourierApi`, `OrderApi`)
- `tests/` — тестовые классы для каждой ручки:
  - `test_create_courier.py` — тесты создания курьера
  - `test_login_courier.py` — тесты логина курьера
  - `test_create_order.py` — тесты создания заказа с параметризацией цветов
  - `test_get_orders.py` — тесты получения списка заказов
- `conftest.py` — фикстуры инициализации клиентов, создания и teardown-очистки тестовых данных
- `data.py` — тестовые данные и константы ошибок
- `helpers.py` — вспомогательные генераторы данных
- `urls.py` — эндпоинты API сервиса
- `target/allure-results/` — результаты тестов для генерации Allure-отчёта

## Запуск тестов
1. Установка зависимостей:
   ```bash
   pip install -r requirements.txt
   ```
2. Запуск тестов со сбором Allure-результатов:
   ```bash
   pytest -v --alluredir=target/allure-results
   ```
3. Просмотр отчёта Allure:
   ```bash
   allure serve target/allure-results
   ```
