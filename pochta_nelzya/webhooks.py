import asyncio
import os

from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot


async def configure_webhook(bot: AsyncTeleBot):
    load_dotenv()
    await bot.remove_webhook()
    await asyncio.sleep(0.1)
    webhook_url = f"{os.getenv('WEBHOOK_URL_PREFIX')}/{os.getenv('BOT_TOKEN')}"
    await bot.set_webhook(url=webhook_url)

