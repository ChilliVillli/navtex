import asyncio
import logging
import sys
from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from bot import router
from aiogram.fsm.strategy import FSMStrategy
from loader import scheduler
from db import sql_start


TOKEN = "5601906129:AAH1k-asnKub2yCS36TUmjHMUlr9UtcarW4"



async def main():

    # sql_start()
    scheduler.start()
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(fsm_strategy=FSMStrategy.USER_IN_CHAT)
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())