import asyncio
from pochta_nelzya.bot import create_bot


async def main():
    bot = await create_bot()
    await bot.polling()

asyncio.run(main())
