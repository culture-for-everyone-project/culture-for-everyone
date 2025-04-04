import asyncio
from aiogram import Bot, Dispatcher

from app.handlers import router
from app.config import BOT_TOKEN
from app.database.models import init_db


async def main():
    await init_db()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router) 
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Бот выключен.')

