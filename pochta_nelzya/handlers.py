from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from pochta_nelzya.db import add_feeding, add_walk, get_all_feedings, get_all_walks
import pochta_nelzya.message_texts as mt


async def add_handlers(bot: AsyncTeleBot):
    @bot.message_handler(commands=['start'])
    async def cmd_start(message: Message):
        await bot.send_message(chat_id=message.chat.id, text=mt.START_MSG)
        await bot.send_message(chat_id=message.chat.id, text=mt.HELP_MSG)

    @bot.message_handler(commands=['help'])
    async def cmd_help(message: Message):
        await bot.send_message(chat_id=message.chat.id, text=mt.HELP_MSG)

    @bot.message_handler(commands=['feed'])
    async def cmd_feed(message: Message):
        add_feeding(by_whom=message.from_user.username)
        await bot.send_message(chat_id=message.chat.id, text=mt.FEED_MSG)

    @bot.message_handler(commands=['all_feedings'])
    async def cmd_all_feedings(message: Message):
        text = mt.ALL_FEEDINGS_MSG + await get_all_feedings()
        await bot.send_message(chat_id=message.chat.id, text=text)

    @bot.message_handler(commands=['walk'])
    async def cmd_walk(message: Message):
        add_walk(by_whom=message.from_user.username)
        await bot.send_message(chat_id=message.chat.id, text=mt.WALK_MSG)

    @bot.message_handler(commands=['all_walks'])
    async def cmd_walk(message: Message):
        text = mt.ALL_WALKS_MSG + await get_all_walks()
        await bot.send_message(chat_id=message.chat.id, text=text)
