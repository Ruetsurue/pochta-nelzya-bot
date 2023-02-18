class MessageTexts:
    START_MSG = "Почта, нельзя!!!!\n" \
                "На дворе 2023, и бот есть у каждой собаки."

    MENU_MSG = "Кормим или гуляем?\n"
    RETURN_TO_MENU_MSG = "Возвращаю в главное меню"

    ASK_FEED_PORTION_SIZE_MSG = "Сколько грамм было в порции? Выбрать вариант / написать свой одним числом"
    FEED_MSG_RESPONSE = "Вот и покормили"
    WALK_MSG_RESPONSE = "Вот и погуляли"

    ASK_RECORD_PERIOD_MSG = "За какой период вывести записи? Выбрать вариант / написать свой одним числом"

    ALL_FEEDINGS_HEADER = "Все кормления: \n"
    FEED_RECORD = "Когда: {time_at}\n" \
                  "Кто: @{by_whom}\n" \
                  "Грамм: {portion_size}"
    ALL_FEEDINGS_MSG = (ALL_FEEDINGS_HEADER, FEED_RECORD)

    ALL_WALKS_HEADER = f"Все выгуливания: \n"
    WALK_RECORD = "Когда: {time_at}\n" \
                  "Кто: @{by_whom}"
    ALL_WALKS_MSG = (ALL_WALKS_HEADER, WALK_RECORD)

    NOT_DIGIT_ERR = "Это не число. Введи число"


class KeyboardButtonCaptions:
    ALL_RECORDS = "Все"
    LAST_DAY_RECORDS = "Последние сутки"

    BACK_TO_MENU = "Назад в меню"
    CANCEL = "Отмена"

    FEED = "Покормить"
    FEED_STANDARD_PORTION_GRAMS = "35"

    SHOW_FEED_RECORDS = "Показать кормления"
    SHOW_WALK_RECORDS = "Показать выгулы"

    WALK = "Выгулять"
