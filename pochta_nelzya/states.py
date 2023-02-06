from telebot.asyncio_handler_backends import StatesGroup, State


class MenuStates(StatesGroup):
    user_requested_menu = State()
    user_selected_option = State()


class FeedDogStates(StatesGroup):
    user_enters_portion_size = State()


class WalkDogStates(StatesGroup):
    pass


class ShowRecordsStates(StatesGroup):
    process_timeperiod_selection = State()
