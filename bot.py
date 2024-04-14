import asyncio
from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from bs4 import BeautifulSoup as bs
import requests
from fake_useragent import UserAgent
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from kb import menu, types_kb
from aiogram.fsm.context import FSMContext
from datetime import datetime


ua = UserAgent()
router = Router()
info = []
# current_date = datetime.now().date()


class Filters(StatesGroup):
    msg_area = State()
    msg_type = State()


@router.message(CommandStart())
async def comand_start_handler(message: Message, state: FSMContext):

    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!", reply_markup=menu)


@router.message(Command(commands=["cancel"]))
@router.message(F.text.lower() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Поиск отменен', reply_markup=menu)


@router.message(F.text == 'Условия для поиска')
async def conditions(message: Message, state: FSMContext):

    await state.set_state(Filters.msg_area)
    await message.answer("Введите условия для поля MSG area! (A-W)")


@router.message(Filters.msg_area)
async def area(message: Message, state: FSMContext):

    await state.update_data(area=message.text.upper())
    await message.answer("Выберите условие для поля MSG type!", reply_markup=types_kb)
    await state.set_state(Filters.msg_type)


@router.message(Filters.msg_type)
async def area(message: Message, state: FSMContext):
    await state.update_data(types=message.text)
    data = await state.get_data()
    Area = data['area']
    Types = data['types']
    await state.clear()

    while True:

        # await asyncio.sleep(2)
        headers = {'User-agent': ua.random}
        session = requests.Session()
        session.headers.update(headers)
        url = 'https://navtex.lv/'
        data_navtex = {'p_date': datetime.now().date(),
                       'p_area': Area,
                       'p_type': Types
                       }
        response = session.post(url, verify=False, data=data_navtex, headers=headers)
        soup = bs(response.text, 'lxml')

        for i in soup.find_all('pre'):

            if i not in info:
                info.append(i.text)
                await message.answer(i.text)
            else:
                continue


async def search():
    pass


