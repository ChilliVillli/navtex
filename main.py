import asyncio
import os

from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from aiogram.fsm.strategy import FSMStrategy
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

from bot import router
from loader import scheduler

load_dotenv("./.env")


TOKEN = os.getenv("TOKEN", "")



async def main():
    scheduler.start()
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(fsm_strategy=FSMStrategy.USER_IN_CHAT)
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    
    asyncio.run(main())