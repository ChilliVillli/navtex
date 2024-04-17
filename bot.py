import asyncio
import requests
from datetime import datetime

from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent


from kb import menu, types_kb
from loader import scheduler


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


# @router.message(F.text == 'Users')
# async def get_user_ids(chat_id):
#     chat_members = await bot.get_chat_members(chat_id)
#     user_ids = [member.user.id for member in chat_members]


@router.message(Command(commands=["cancel"]))
@router.message(F.text.lower() == "отмена")
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
    await message.answer("Выберите условие для поля MSG type или выберите '*' для условия по умолчанию", reply_markup=types_kb)
    await state.set_state(Filters.msg_type)


@router.message(Filters.msg_type)
async def types_state(message: Message, state: FSMContext):
    await state.update_data(types=message.text)
    data = await state.get_data()
    area = data['area']
    types = data['types']
    await state.clear()


    # Тут Задачу запускаем в первый раз для сбора данных
    await example_search(message, area, types, True)
    # Тут Задачу закидываем чтобы она проверяла что то новое
    scheduler.add_job(example_search, "interval", seconds=5, args=(message, area, types, False))


    # А это запусти
    # await search(message, area, types, True)
    # scheduler.add_job(search, "interval", seconds=5, args=(message, area, types, False))


async def example_search(message, area, types, first):
    """Просто потом удали эту функцию))"""
    
    if not first:
        await message.answer("Задача интервальная")


async def get_soup(area, types):
    """Получить "soup".
    Функция делает запрос к ресурсу, 
    создает и возвращает объект Beautiful Soup.
    """

    headers = {'User-agent': ua.random}
    session = requests.Session()
    session.headers.update(headers)
    url = 'https://navtex.lv/'
    data_navtex = {'p_date': datetime.now().date(),
                   'p_area': area,
                   'p_type': types
                   }
    response = session.post(url, verify=False, data=data_navtex, headers=headers)
    await asyncio.sleep(1)
    soup = bs(response.text, 'lxml')
    return soup


async def search(message, area, types, first):
    """Мне кажется достаточно этой функции, просто запускать её каждый раз и все
    Она все равно отправляет сообщение только тогда когда что то новое находит
    """
    soup = await get_soup(area, types)

    for i in soup.find_all('pre'):

        description = i.text
        # await asyncio.sleep(1)

        for count, j in enumerate(soup.find_all('h4')):

            if count == 0:
                continue

            data_time = j.text

            if data_time not in info:
                if not first:
                    await message.answer(description)
                # print(f"{data_time}\n{description}")
                info.append(data_time)
                # await asyncio.sleep(2)
                break
            else:
                continue
