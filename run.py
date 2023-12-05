import sys
import logging
import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from app.handlers import router


async def main():
    bot = Bot(token=TOKEN, parse_mode="Markdown")
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")
