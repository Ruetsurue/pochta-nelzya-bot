import os
import dotenv
import telebot.async_telebot
from flask import Flask, request, abort
from pochta_nelzya.webhooks import configure_webhook


async def setup_routes(app: Flask, bot: telebot.async_telebot.AsyncTeleBot):
    dotenv.load_dotenv()
    BOT_WEBHOOK_URL = f"/{os.getenv('BOT_TOKEN')}"

    @app.route(BOT_WEBHOOK_URL, methods=["POST"])
    async def read_and_process_update():
        if request.content_type == "application/json":
            json = request.get_json()
            update = telebot.types.Update.de_json(json)
            await bot.process_new_updates(updates=[update])
            return '', 200

        else:
            abort(code=409, response={"message": "json expected but other content_type received"})

    @app.route('/')
    async def setup_webhook():
        await configure_webhook(bot)
