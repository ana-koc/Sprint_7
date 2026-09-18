class CourierData:
    # Ошибки из технической документации Swagger
    ERROR_CREDENTIALS_REQUIRED = "Недостаточно данных для создания учетной записи"
    ERROR_LOGIN_ALREADY_EXISTS = "Этот логин уже используется. Попробуйте другой."
    ERROR_LOGIN_CREDENTIALS_REQUIRED = "Недостаточно данных для входа"
    ERROR_ACCOUNT_NOT_FOUND = "Учетная запись не найдена"
    ERROR_DELETE_WITHOUT_ID = "Недостаточно данных для удаления курьера"
    ERROR_DELETE_NOT_FOUND = "Курьера с таким id нет"


class OrderData:
    # Шаблон данных для создания заказа
    DEFAULT_ORDER_BODY = {
        "firstName": "Наруто",
        "lastName": "Учиха",
        "address": "Коноха, 142",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2026-12-31",
        "comment": "Позвонить за 15 минут",
        "color": []
    }

    # Наборы цветов для параметризации
    COLOR_OPTIONS = [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ]
