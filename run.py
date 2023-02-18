from dotenv import load_dotenv
from fastapi import FastAPI

from pochta_nelzya.bot import Bot
from pochta_nelzya.models import async_engine as db_engine
from pochta_nelzya.routes import setup_routes


load_dotenv()
app = FastAPI()
b = Bot()


@app.on_event("startup")
async def startup_event():
    await b.create_bot()
    await setup_routes(app=app, bot=b.bot)


@app.on_event("shutdown")
async def shutdown_event():
    try:
        await b.bot.remove_webhook()
    finally:
        await b.bot.close_session()
        await b.bot.close()
        await db_engine.dispose()




