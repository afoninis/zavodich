# import logging
import asyncio

from aiogram import Bot, Dispatcher

from settings import *
from app.handlers import router


# logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(router=router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот ложится отдыхать 🛏️")
