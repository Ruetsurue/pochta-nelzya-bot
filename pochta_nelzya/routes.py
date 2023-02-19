import asyncio
import logging
import os

from fastapi import FastAPI, Request, status
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Update


async def setup_routes(app: FastAPI, bot: AsyncTeleBot):
    @app.get('/', status_code=status.HTTP_200_OK, response_model=None)
    async def create_app():
        await bot.remove_webhook()
        webhook_url = f"{os.getenv('WEBHOOK_URL_PREFIX')}/{os.getenv('BOT_TOKEN')}"
        await asyncio.sleep(0.1)
        await bot.set_webhook(url=webhook_url,
                              drop_pending_updates=True,
                              max_connections=3,
                              allowed_updates=['message'])
        logging.info('Bot successfully launched')
        return

    @app.post(f"/{os.getenv('BOT_TOKEN')}", status_code=status.HTTP_200_OK, response_model=None)
    async def receive_and_process_update(req: Request):
        update = await req.json()
        logging.debug(f'NEW UPDATE:\n\n{update}')
        update = Update.de_json(update)
        await bot.process_new_updates(updates=[update])
        return
