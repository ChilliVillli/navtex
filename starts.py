import asyncio
from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from bot import router
from aiogram.fsm.strategy import FSMStrategy


TOKEN = "5601906129:AAH1k-asnKub2yCS36TUmjHMUlr9UtcarW4"



async def main():

    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(fsm_strategy=FSMStrategy.USER_IN_CHAT)
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())