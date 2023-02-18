import logging
import os

from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message


def configure_logging():
    load_dotenv()

    LOGLEVEL = logging.getLevelName(os.getenv('LOGLEVEL'))
    log_format = '%(asctime)s %(levelname)s: %(message)s'
    log_time_format = '%d.%m.%Y %H:%M:%S %z'
    logging.basicConfig(level=LOGLEVEL, format=log_format, datefmt=log_time_format)


def log_cmd(user, command):
    message = f"{user} {command}"
    logging.debug(message)


async def log_state(bot: AsyncTeleBot, message: Message):
    state = await bot.get_state(message.from_user.id, message.chat.id)
    logging.debug(f'Current bot state of user {message.from_user.username}: {state}')
