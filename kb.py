from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu_admin = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Условия для поиска'),
            KeyboardButton(text='Users')
        ]
    ],
    resize_keyboard=True
)

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Условия для поиска')
        ]
    ],
    resize_keyboard=True
)


types_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='A (Navigational warnings)'),
            KeyboardButton(text='B (Meteorological warnings)'),
            KeyboardButton(text='C (Ice reports)')
        ],
        [
            KeyboardButton(text='D (SAR)'),
            KeyboardButton(text='E (Meteorological forecasts)'),
            KeyboardButton(text='F (Pilot service messages)')
        ],
        [
            KeyboardButton(text='G (AIS)'),
            KeyboardButton(text='H (LORAN messages)'),
            KeyboardButton(text='L (Navigational warnings)')
        ],
        [
            KeyboardButton(text='*')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


cancel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='отмена поиска')
        ]
    ],
    resize_keyboard=True
)