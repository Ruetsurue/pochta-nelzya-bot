import os
import logging

import flask
from telebot.async_telebot import AsyncTeleBot, StateMemoryStorage
from dotenv import load_dotenv

from pochta_nelzya.models import create_db_objects
from pochta_nelzya.msg_handlers import add_handlers
from pochta_nelzya.logs import configure_logging
from pochta_nelzya.webhooks import configure_webhook
from pochta_nelzya.routes import setup_routes


async def create_bot(app: flask.Flask) -> AsyncTeleBot:
    load_dotenv()
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    bot = AsyncTeleBot(token=BOT_TOKEN, state_storage=StateMemoryStorage())
    await create_db_objects()
    await add_handlers(bot)
    await configure_webhook(bot)
    await setup_routes(app=app, bot=bot)
    configure_logging()
    logging.info('Bot successfully launched')

    return bot
