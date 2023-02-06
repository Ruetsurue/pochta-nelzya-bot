import logging

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
from telebot.asyncio_filters import StateFilter

from pochta_nelzya.msg_texts import MessageTexts as mt, KeyboardButtonCaptions as cpt
from pochta_nelzya.msg_formatters import get_all_records_for_n_days
from pochta_nelzya.models import FeedDogModel, WalkDogModel
from pochta_nelzya.logs import log_cmd
from pochta_nelzya.states import MenuStates, FeedDogStates, ShowRecordsStates
from pochta_nelzya.keyboards import BotKeyboards


async def add_handlers(bot: AsyncTeleBot):
    bot.add_custom_filter(custom_filter=StateFilter(bot))

    @bot.message_handler(commands=['start'])
    async def cmd_start(message: Message):
        log_cmd(message.from_user.username, message.text)
        await bot.send_message(message.chat.id, mt.START_MSG)
        await bot.reply_to(message, text=mt.MENU_MSG, reply_markup=BotKeyboards.main_menu_markup())
        await bot.set_state(user_id=message.from_user.id, state=MenuStates.user_selected_option,
                            chat_id=message.chat.id)

    @bot.message_handler(state=MenuStates.user_requested_menu)
    async def show_menu(message: Message):
        log_cmd(message.from_user.username, message.text)

        # reset bot context each time a new operation is invoked to clear previous operations' leftovers
        await bot.reset_data(message.from_user.id, message.chat.id)

        await bot.reply_to(message, text=mt.MENU_MSG, reply_markup=BotKeyboards.main_menu_markup())
        await bot.set_state(user_id=message.from_user.id, state=MenuStates.user_selected_option,
                            chat_id=message.chat.id)

    @bot.message_handler(state=MenuStates.user_selected_option)
    async def execute_selected_option(message: Message):
        log_cmd(message.from_user.username, message.text)

        if message.text == cpt.FEED:
            await start_feed_msg_chain(message=message)

        elif message.text == cpt.WALK:
            await start_walk_msg_chain(message=message)

        elif message.text == cpt.SHOW_FEED_RECORDS:
            async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['use_model'] = FeedDogModel
                data['msg_template'] = mt.ALL_FEEDINGS_MSG
            await start_show_record_msg_chain(message=message)

        elif message.text == cpt.SHOW_WALK_RECORDS:
            async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['use_model'] = WalkDogModel
                data['msg_template'] = mt.ALL_WALKS_MSG
            await start_show_record_msg_chain(message=message)

    async def start_feed_msg_chain(message: Message):
        await bot.reply_to(message, text=mt.ASK_FEED_PORTION_SIZE_MSG,
                           reply_markup=BotKeyboards.feed_portion_size_options_markup())
        await bot.set_state(message.from_user.id, FeedDogStates.user_enters_portion_size, message.chat.id)

    @bot.message_handler(state=FeedDogStates.user_enters_portion_size)
    async def process_portion_size_and_save(message: Message):
        keyboard = BotKeyboards.finish_operation_and_return_to_menu_markup()
        state = MenuStates.user_requested_menu

        if message.text == cpt.CANCEL:
            text = mt.RETURN_TO_MENU_MSG

        elif message.text.isdigit():
            by_whom, portion_size = message.from_user.username, message.text
            log_cmd(by_whom, message.text)
            feeding = FeedDogModel(by_whom=by_whom, portion_size=portion_size)
            logging.debug(feeding)
            await feeding.save_to_db()
            logging.info(msg=f'{by_whom} created feed record of {portion_size} grams')
            text = mt.FEED_MSG_RESPONSE

        # exit and retry if invalid input
        else:
            await bot.reply_to(message, text=mt.NOT_DIGIT_ERR,
                               reply_markup=BotKeyboards.feed_portion_size_options_markup())
            return

        await bot.reply_to(message, text=text, reply_markup=keyboard)
        await bot.set_state(user_id=message.from_user.id, state=state, chat_id=message.chat.id)

    async def start_show_record_msg_chain(message: Message):
        await bot.reply_to(message, text=mt.ASK_RECORD_PERIOD_MSG,
                           reply_markup=BotKeyboards.show_records_for_num_days_markup())
        await bot.set_state(message.from_user.id, ShowRecordsStates.process_timeperiod_selection, message.chat.id)

    @bot.message_handler(state=ShowRecordsStates.process_timeperiod_selection)
    async def process_timeperiod_selection(message: Message):
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            model = data['use_model']
            msg_template = data['msg_template']

        if message.text == cpt.CANCEL:
            text = mt.RETURN_TO_MENU_MSG

        elif message.text == cpt.ALL_RECORDS:
            text = await get_all_records_for_n_days(model=model, msg_template=msg_template, show_all=True)

        elif message.text == cpt.LAST_DAY_RECORDS:
            text = await get_all_records_for_n_days(model=model, msg_template=msg_template, for_days=1)

        elif message.text.isdigit():
            text = await get_all_records_for_n_days(model=model, msg_template=msg_template, for_days=int(message.text))

        # exit and retry if invalid input
        else:
            await bot.reply_to(message, text=mt.NOT_DIGIT_ERR,
                               reply_markup=BotKeyboards.show_records_for_num_days_markup())
            return

        await bot.reply_to(message, text=text, reply_markup=BotKeyboards.finish_operation_and_return_to_menu_markup())
        await bot.set_state(user_id=message.from_user.id, state=MenuStates.user_requested_menu, chat_id=message.chat.id)

    async def start_walk_msg_chain(message: Message):
        by_whom = message.from_user.username
        log_cmd(by_whom, message.text)

        walk = WalkDogModel(by_whom=by_whom)
        logging.debug(walk)
        await walk.save_to_db()
        logging.info(f'{by_whom} recorded a walk')

        await bot.reply_to(message, text=mt.WALK_MSG_RESPONSE,
                           reply_markup=BotKeyboards.finish_operation_and_return_to_menu_markup())
        await bot.set_state(user_id=message.from_user.id, state=MenuStates.user_requested_menu, chat_id=message.chat.id)
