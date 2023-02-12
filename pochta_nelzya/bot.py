import os
import logging

from telebot.async_telebot import AsyncTeleBot, StateMemoryStorage
from dotenv import load_dotenv

from pochta_nelzya.models import create_db_objects
from pochta_nelzya.msg_handlers import add_handlers
from pochta_nelzya.logs import configure_logging


async def create_bot() -> AsyncTeleBot:
    load_dotenv()
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    bot = AsyncTeleBot(token=BOT_TOKEN, state_storage=StateMemoryStorage())
    await create_db_objects()
    await add_handlers(bot)
    configure_logging()
    logging.info('Bot successfully launched')

    return bot
