import asyncio
from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from bs4 import BeautifulSoup as bs
import requests
from fake_useragent import UserAgent
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from kb import menu, types_kb, menu_admin, cancel
from aiogram.fsm.context import FSMContext
from datetime import datetime
from loader import scheduler
from db import sql_start, count_id


ua = UserAgent()
router = Router()
info = []


class Filters(StatesGroup):
    msg_area = State()
    msg_type = State()


@router.message(CommandStart())
async def comand_start_handler(message: Message, state: FSMContext):

    userid = message.from_user.id

    if userid == 2010885045:
        await message.answer(f"Hello, {hbold(message.from_user.full_name)}!", reply_markup=menu_admin)
    else:
        await message.answer(f"Hello, {hbold(message.from_user.full_name)}!", reply_markup=menu)
        await sql_start(userid)


@router.message(F.text == 'Users')
async def sql_user_id(message: Message):

    await message.answer(f"Активировало бота - {count_id()} пользователей!", reply_markup=menu)


@router.message(Command(commands=["cancel"]))
@router.message(F.text.lower() == "отмена поиска")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Поиск отменен', reply_markup=menu)


@router.message(F.text == 'Условия для поиска')
async def conditions(message: Message, state: FSMContext):

    await state.set_state(Filters.msg_area)
    await message.answer("Введите условия для поля MSG area! (A-W) или введите '*' для условия по умолчанию")


@router.message(Filters.msg_area)
async def area_state(message: Message, state: FSMContext):

    await state.update_data(area=message.text.upper())

    if message.text.upper() in 'ABCDEFGHIJKLMNOPQRSTUVW*' and len(message.text) == 1:
        await message.answer("Выберите условие для поля MSG type или выберите '*' для условия по умолчанию", reply_markup=types_kb)
        await state.set_state(Filters.msg_type)
    else:
        await message.answer("❌ Вы ввели неправильный символ!"
                             "\nВведите повторно условие для поля MSG area! (A-W) или введите '*' для условия по умолчанию")
        await state.set_state(Filters.msg_area)


@router.message(Filters.msg_type)
async def types_state(message: Message, state: FSMContext):
    await state.update_data(types=message.text)
    data = await state.get_data()
    area = data['area']
    types = data['types']
    await state.clear()
    await message.answer("Приступаю к поиску!", reply_markup=cancel)
    await search(message, area, types, True)
    scheduler.add_job(search, "interval", seconds=60, args=(message, area, types, False))


async def get_soup(area, types):

    headers = {'User-agent': ua.random}
    session = requests.Session()
    session.headers.update(headers)
    url = 'https://navtex.lv/'
    data_navtex = {'p_date': datetime.now().date(),
                   'p_area': area,
                   'p_type': types
                   }
    response = session.post(url, verify=False, data=data_navtex, headers=headers)
    await asyncio.sleep(2)
    soup = bs(response.text, 'lxml')


    for count, j in enumerate(soup.find_all('h4')):

        if count == 0:
            continue

        data_time = j.text

        if data_time not in info:
            info.append(data_time)
            print(data_time)
            # await asyncio.sleep(3)
        else:
            continue

    return soup


async def search(message, area, types, first):

    soup = await get_soup(area, types)

    await asyncio.sleep(1)

    for i in soup.find_all('pre'):

        description = i.text
        await asyncio.sleep(1)

        for count, j in enumerate(soup.find_all('h4')):

            if count == 0:
                continue

            data_time = j.text

            if data_time not in info:
                await message.answer(f"{data_time}\n{description}")
                if not first:
                    await message.answer(description)
                info.append(data_time)
                await asyncio.sleep(2)
                break
            else:
                continue