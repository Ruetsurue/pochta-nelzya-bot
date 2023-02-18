import os
import logging

from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot, StateMemoryStorage
from typing import Optional

from pochta_nelzya.models import create_db_objects
from pochta_nelzya.msg_handlers import add_handlers
from pochta_nelzya.logs import configure_logging


class Bot:
    def __init__(self):
        self._bot: Optional[AsyncTeleBot] = None

    @property
    def bot(self):
        return self._bot

    def set_bot(self, new_bot):
        if self._bot is None:
            self._bot = new_bot

    async def create_bot(self) -> AsyncTeleBot:
        load_dotenv()
        BOT_TOKEN = os.getenv('BOT_TOKEN')
        new_bot = AsyncTeleBot(token=BOT_TOKEN, state_storage=StateMemoryStorage())
        await create_db_objects()
        await add_handlers(new_bot)
        configure_logging()
        self.set_bot(new_bot)
        logging.info('Bot successfully created')

        return new_bot
