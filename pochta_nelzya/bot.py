import os

from telebot.async_telebot import AsyncTeleBot
from dotenv import load_dotenv

from pochta_nelzya.handlers import add_handlers


async def create_bot() -> AsyncTeleBot:
    load_dotenv()
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    bot = AsyncTeleBot(token=BOT_TOKEN)
    await add_handlers(bot)

    return bot