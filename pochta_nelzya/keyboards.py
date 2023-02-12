from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from pochta_nelzya.msg_texts import KeyboardButtonCaptions as cpt


class BotKeyboards:

    @staticmethod
    def main_menu_markup():
        kb = ReplyKeyboardMarkup(row_width=2)
        kb.add(KeyboardButton(cpt.FEED),
               KeyboardButton(cpt.WALK),
               KeyboardButton(cpt.SHOW_FEED_RECORDS),
               KeyboardButton(cpt.SHOW_WALK_RECORDS))
        return kb

    @staticmethod
    def feed_portion_size_options_markup():
        kb = ReplyKeyboardMarkup()
        kb.add(KeyboardButton(cpt.FEED_STANDARD_PORTION_GRAMS),
               KeyboardButton(cpt.CANCEL))
        return kb

    @staticmethod
    def show_records_for_num_days_markup():
        kb = ReplyKeyboardMarkup()
        kb.add(KeyboardButton(cpt.LAST_DAY_RECORDS),
               KeyboardButton(cpt.ALL_RECORDS),
               KeyboardButton(cpt.CANCEL))
        return kb

    @staticmethod
    def finish_operation_and_return_to_menu_markup():
        kb = ReplyKeyboardMarkup()
        kb.add(KeyboardButton(cpt.BACK_TO_MENU))
        return kb
