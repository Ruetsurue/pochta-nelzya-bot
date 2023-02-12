import asyncio
from flask import Flask
from pochta_nelzya.bot import create_bot


async def create_app():
    app = Flask(import_name=__name__)
    bot = await create_bot(app)
    # await bot.polling()
    return app

app = asyncio.run(create_app())
